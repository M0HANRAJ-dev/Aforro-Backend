from django.test import TestCase
from rest_framework.test import APIClient
from products.models import Category, Product

class SearchTestCase(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        
        self.category = Category.objects.create(name="Mobiles")
        
        Product.objects.create(
            title="iPhone",
            price=80000,
            category=self.category
        )
        
    def test_search_products(self):
        response = self.client.get("/api/search/products/?q=iphone")
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data["results"]) > 0)
