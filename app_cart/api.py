from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from app_main.models import Product


class CartView(APIView):
    def get(self, request, session_id):
        # Construct the cache key using the session ID
        cache_key = f'{session_id}'
        # Retrieve the shopping cart from the cache
        shopping_cart = cache.get(cache_key) or {}
        # Calculate the total price of the products in the shopping cart
        total = 0
        products = Product.objects.in_bulk(shopping_cart.keys())
        for product in products.values():
            total += (product.price * shopping_cart[str(product.id)])
        # Return the shopping cart as a JSON response
        return Response({
            'products': shopping_cart,
            'total': total,
            'cantReal': len(shopping_cart)
        })
