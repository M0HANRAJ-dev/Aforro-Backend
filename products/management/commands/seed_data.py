from django.core.management.base import BaseCommand
from faker import Faker
import random
from product.models import Category, Product
from stores.models import Store, Inventory

fake = Faker()

class Command(BaseCommand):
    help = "Seed database with dummy data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding started...")

        categories = []
        for _ in range(10):
            category = Category.objects.create(
                name=fake.word()
            )
            categories.append(category)
        
        self.stdout.write("Categories created")

        products = []
        for _ in range(1000):
            product = Product.objects.create(
                title=fake.word() + " " + fake.word(),
                description=fake.text(),
                price=random.randint(100, 10000),
                category=random.choice(categories)
            )
            products.append(product)
        
        self.stdout.write("Products created")

        Stores = []
        for _ in range(20):
            store = Store.objects.create(
                name=fake.company(),
                location=fake.city()
            )
            stores.append(store)

        self.stdout.write("Stores created")

        for store in stores:
            selected_products = random.sample(products, 300)

            for product in selected_products:
                Inventory.objects.create(
                    store=store,
                    product=product,
                    quantity=random.randint(0, 50)
                )

        self.stdout.write(self.style.SUCCESS('Seeding completed successfulluy'))