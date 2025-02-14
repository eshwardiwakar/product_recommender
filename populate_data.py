import os
import django
import random
from django.utils import timezone

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'product_recommender.settings')
django.setup()

# Import models after setting up Django
from recommender.models import Product, Order

def create_products():
    """Create random products."""
    for i in range(10):  # Create 10 random products
        Product.objects.create(
            name=f'Product {i}',
            description=f'Description for Product {i}',
            price=round(random.uniform(10, 100), 2),  # Random price between 10 and 100
        )
    print("Created 10 random products.")

def create_orders():
    """Create random orders."""
    products = list(Product.objects.all())
    for i in range(5):  # Create 5 random orders
        order = Order.objects.create(
            total_amount=0,  # Initialize total amount
            created_at=timezone.now(),
        )
        selected_products = random.sample(products, 3)  # Randomly select 3 products
        order.products.set(selected_products)
        order.total_amount = sum(p.price for p in selected_products)  # Calculate total amount
        order.save()
    print("Created 5 random orders.")

if __name__ == '__main__':
    create_products()
    create_orders()