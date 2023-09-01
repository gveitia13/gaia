from django.urls import path

from app_cart.api import CartView
from app_cart.views import *

urlpatterns = [
    path("cart/add/<id>/", add, name="cart_add"),
    path("cart/add/<id>/<int:quantity>/", add_quant, name="cart_add_quantity"),
    path("cart/decrement/<id>/<int:quantity>/", decrement_quant, name="cart_decrement_quantity"),
    path("cart/remove/<id>/", remove, name="cart_remove"),
    # actualizar cantidad
    path('cart/update_quantity/<id>/<value>/', update_quant, name='cart_update_quantity'),
    path('cart/update_quantity/bl/<id>/<value>/', update_quant_bl, name='cart_update_quantity_bl'),
    path("cart/remove/<id>/<quantity>/", remove_quant, name="cart_remove_quantity"),
    path("cart/clear/", cart_clear, name="cart_clear"),
    path("cart/pop/", cart_pop, name="cart_pop"),
    path("cart/clear/<id>/", item_clear, name="cart_clear_id"),
    path("cart/details/<id>/", cart_detail, name="cart_detail"),
    path('cart/<str:session_id>/', CartView.as_view()),
]
