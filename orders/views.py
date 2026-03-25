from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import Order, OrderItem
from store.models import Store, Inventory
from product.models import Product
from rest_framework.views import APIView
from django.db.models import Count
from Stores.models import Store
from .tasks import send_order_confirmation

class CreateOrderAPIView(APIView):
    def post(self, request):
        data = request.data
        store_id = data.get("store_id")
        items = data.get("items", [])

        try:
            store = Store.objects.get(id=store_id)
        except Store.DoesNotExist:
            return Response({"error": "Store not found"}, status=404)

        with transaction.atomic():
            insufficient = False
            inventory_map = []

            for item in items:
                product_id = item["product_id"]
                qty = item["quantity_requested"]

                try:
                    inventory = Inventory.objects.select_for_update().get(
                        store=store,
                        product_id=product_id
                    )
                except Inventory.DoesNotExist:
                    insufficient = True
                    break

                if inventory.quantity < qty:
                    insufficient = True
                    break
                
                inventory_map.append((inventory, qty))

            if insufficient:
                order = Order.objects.create(
                    store=store,
                    status=Order.Status.REJECTED
                )
                return Response({
                    "message": "Order rejected due to insufficient stock",
                    "order_id": order.id,
                    "status": order.status
                }, status=400)

            for inventory, qty in inventory_map:
                inventory.quantity -= qty
                inventory.save()

            order = Order.objects.create(
                store=store,
                status=Order.Status.CONFIRMED
            )

            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product_id=item["product_id"],
                    quantity_requested=item["quantity_requested"]
                )

            send_order_confirmation.delay(order.id)
            
            return Response({
                "message": "Order confirmed",
                "order_id": order.id,
                "status": order.status
            }, status=201)

class StoreOrderAPIView(APIView):
    def get(self, request, store_id):
        try:
            store = Store.objects.get(id=store_id)
        except Store.DoesNotExist:
            return Response({"error": "Store not found"}, status=404)

        orders = (
            Order.objects
            .filter(store=store)
            .annotate(item_count=Count('items'))
            .order_by("-created_at")
        )

        data = []
        for order in orders:
            data.append({
                "order_id": order.id,
                "status": order.status,
                "created_at": order.created_at,
                "total_items": order.item_count
            })
        return Response(data)