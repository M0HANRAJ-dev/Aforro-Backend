from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from django.core.paginator import Paginator
from products.models import Product
from stores.models import Inventory
from django.core.cache import cache
import hashlib

class ProductSearchAPIView(APIView):
    def get(self, request):
        query_string = request.META.get("QUERY_STRING", "")
        cache_key = f"search:{hashlib.md5(query_string.encode()).hexdigest()}"

        cache_data = cache.get(cache_key)
        if cache_data:
            return Response(cache_data)

        query = request.GET.get("q","")
        category = request.GET.get("category")
        min_price = request.GET.get("min_price")
        max_price = request.GET.get("max_price")
        store_id = request.GET.get("store_id")
        in_stock = request.GET.get("in_stock")
        sort = request.GET.get("sort", "newest")

        products = Product.objects.all().select_related('category')

        if query:
            products = product.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query)
            )

        if category:
            products = products.filter(category__id=category)

        if min_price:
            products = products.filter(price__gte=min_price)
        
        if max_price:
            products = products.filter(price__lte=max_price)

        if store_id:
            products = products.filter(inventory__store_id=store_id)
        
        if in_stock == 'true':
            products = products.filter(inventory__quantity__gt=0)

        if sort == 'price':
            products = products.order_by("price")
        elif sort == 'newest':
            products = products.order_by("-created_at")

        products = products.distinct()

        page = int(request.GET.get("page", 1))
        page_size = int(request.GET.get('page_size', 10))
        
        paginator = Paginator(product, page_size)
        page_obj = paginator.get_page(page)

        data = []
        for product in page_obj:
            item = {
                'id': product.id,
                'title': product.title,
                'price': product.price,
                'category': product.category.name,
            }

            if store_id:
                inventory = Inventory.objects.filter(
                    store_id=store_id,
                    product=product
                ).first()

                item["quantity"] = inventory.quantity if inventory else 0

            data.append(item)

        return Response({
            'total': paginator.count,
            'page': page,
            'page_size': page_size,
            'results': data
        })

        cache.set(cache_key, response_date, timeout=60*5)

        return Response(response_date)

class ProductSuggestAPIView(APIView):
    def get(self, request):
        q = request.GET.get('q', '').strip()
        
        if len(q) < 3:
            return Response({
                "error": "Minimum 3 charecters required"
            }, status=400)

        prefix_matches = Product.objects.filter(
            title__istartswith=q
        ).values_list('title', flat=True)[:10]

        remaining = 10 - len(prefix_matches)

        other_matches = []
        if remaining > 0:
            other_matches = Product.objects.filter(
                title__icontains=q
            ).exclude(
                title__istartswith=q
            ).values_list('title', flat=True)[:remaining]

        suggestions = list(prefix_matches) + list(other_matches)

        return Response({
            "suggestions": suggestions
        })