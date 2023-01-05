from django.urls import path

from app_cart.views import *

urlpatterns = [
    path("cart/add/<id>/", add, name="cart_add"),
    path("cart/add/<id>/<quantity>/", add_quant, name="cart_add_quantity"),
    path("cart/remove/<id>/", remove, name="cart_remove"),
    # actualizar cantidad
    path('cart/update_quantity/<id>/<value>/', update_quant, name='cart_update_quantity'),

    path("cart/remove/<id>/<quantity>/", remove_quant, name="cart_remove_quantity"),
    path("cart/clear/", cart_clear, name="cart_clear"),
    path("cart/pop/", cart_pop, name="cart_pop"),
    path("cart/clear/<id>/", item_clear, name="cart_clear_id"),
    path("cart/details/<id>/", cart_detail, name="cart_detail"),
    # path("cart/update/", update_cart, name="cart_update"),
]
