from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Store, Inventory

class StoreInventoryAPIView(APIView):
    def get(self, request, store_id):
        try:
            store = Store.objects.get(id=store_id)
        except Store.DoesNotExist:
            return Response({"error": "Store not found"}, status=404)
        
        inventory = (
            Inventory.objects
            .filter(store=store)
            .select_related('product', 'product__category')
            .order_by('product_title')
        )
        data = []
        for item in inventory:
            data.append({
                "product_title": item.product.title,
                "price": item.product.price,
                "category": item.product.category.name,
                "quantity": item.quantity
            })

        return Response(data)