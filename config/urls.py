"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from orders.views import CreateOrderAPIView, StoreOrdersAPIView
from stores.views import StoreInventoryAPIView
from search.views import ProductSearchAPIView, ProductSuggestAPIView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Orders
    path('orders/', CreateOrderAPIView.as_view()),
    path('stores/<int:store_id>/orders/', StoreOrdersAPIView.as_view()),

    # Inventory
    path('stores/<int:store_id>/inventory/', StoreInventoryAPIView.as_view()),

    # Search
    path('api/search/products/', ProductSearchAPIView.as_view()),
    path('api/search/suggest/', ProductSuggestAPIView.as_view()),
]
