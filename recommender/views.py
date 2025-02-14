from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def order_list(request):
    if request.method == 'GET':
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'GET':
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from django.db.models import Count

@api_view(['POST'])
def recommend_products(request):
    product_ids = request.data.get('product_ids', [])
    if not product_ids:
        return Response({'error': 'No product IDs provided'}, status=status.HTTP_400_BAD_REQUEST)

    # Find orders that contain the provided products
    orders = Order.objects.filter(products__in=product_ids).distinct()
    
    # Find products that are frequently bought together
    recommended_products = Product.objects.filter(orders__in=orders).exclude(id__in=product_ids)
    recommended_products = recommended_products.annotate(num_orders=Count('orders')).order_by('-num_orders')[:5]

    serializer = ProductSerializer(recommended_products, many=True)
    return Response(serializer.data)       
"""""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product  # Assuming your product model is here
from .serializers import ProductSerializer

@api_view(['GET'])
def recommend_products(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)

    # Example: Find products with similar price (within ±10% of the given product)
    min_price = float(product.price) * 0.9
    max_price = float(product.price) * 1.2
    recommended_products = Product.objects.filter(price__gte=min_price, price__lte=max_price).exclude(id=product_id)

    # Serialize and return the recommended products
    serializer = ProductSerializer(recommended_products, many=True)
    return Response(serializer.data)
    """
from collections import Counter
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .models import Product, Order
from .serializers import ProductSerializer

@api_view(['GET'])
def recommend_products(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)

    # Get all orders that include this product
    orders = Order.objects.filter(products=product)

    # Count the frequency of products appearing in the same orders
    product_counts = Counter()
    for order in orders:
        for p in order.products.exclude(id=product_id):
            product_counts[p.id] += 1  # Use product ID instead of object

    # Get the most frequently bought together products (Top 5)
    recommended_product_ids = [p[0] for p in product_counts.most_common(15)]
    recommended_products = Product.objects.filter(id__in=recommended_product_ids)

    # Fallback: If no frequently bought together products exist, recommend random products
    if not recommended_products.exists():
        recommended_products = Product.objects.order_by('?')[:15]  # Select 5 random products

    # Serialize and return JSON response
    serializer = ProductSerializer(recommended_products, many=True)
    return JsonResponse(serializer.data, safe=False)  # Force JSON response




