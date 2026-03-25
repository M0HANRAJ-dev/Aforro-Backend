from django.test import TestCase
from rest_framework.test import APIClient
from products.models import Category, Product
from stores.models import Store, Inventory

class InventoryTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(title="Laptop", price=50000, category=self.category)
        self.store = Store.objects.create(name="Mumbai Store", location="Mumbai")
        Inventory.objects.create(store=self.store, product=self.product, quantity=5)

    def test_inventory_listing(self):
        response = self.client.get(f'/stores/{self.store.id}/inventory/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['product_title'], 'Laptop')

    def test_store_not_found(self):
        response = self.client.get('/stores/9999/inventory/')
        self.assertEqual(response.status_code, 404)
