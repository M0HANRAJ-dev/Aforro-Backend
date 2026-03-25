from django.test import TestCase
from rest_framework.test import APIClient
from products.models import Category, Product
from stores.models import Store, Inventory

class OrderTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.category = Category.objects.create(name="Electronics")
        
        self.product = Product.objects.create(
            title="Phone",
            price=10000,
            category=self.category
        )
        
        self.store = Store.objects.create(
            name="Chennai Store",
            location="Chennai"
        )
        
        self.inventory = Inventory.objects.create(
            store=self.store,
            product=self.product,
            quantity=10
        )
        
    def test_order_success(self):
        data = {
            "store_id": self.store.id,
            "items": [
                {
                    "product_id": self.product.id,
                    "quantity_requested": 2
                }
            ]
        }
        
        response = self.client.post('/orders/', data, format='json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["status"], "CONFIRMED")
        
    def test_order_rejected(self):
        data = {
            "store_id": self.store.id,
            "items": [
                {
                    "product_id": self.product.id,
                    "quantity_requested": 20
                }
            ]
        }
        
        response = self.client.post('/orders/', data, format='json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["status"], "REJECTED")
