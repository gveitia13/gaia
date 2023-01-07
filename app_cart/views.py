import json

from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from app_cart.cart import Cart
from app_main.models import Product
from gaia.settings import CART_SESSION_ID


@require_POST
# @method_decorator(csrf_exempt, require_POST)
def add(request: HttpRequest, id: int):
    cart = Cart(request)
    cart.add(product=Product.objects.filter(id=id).first())
    # print(str(cart))
    for i in cart.all():
        print(i)
    return JsonResponse({
        'product': Product.objects.get(id=id).toJSON(),
        "result": "ok",
        "amount": cart.session[CART_SESSION_ID].get(id, {"quantity": 0})["quantity"]
    })


@require_POST
def cart_detail(request: HttpRequest, id: int):
    return JsonResponse({"result": Cart(request).get_item(id)})


@require_POST
def cart_clear(request: HttpRequest):
    Cart(request).clear()
    return JsonResponse({"result": "ok", "amount": 0})


@require_POST
# @method_decorator(csrf_exempt, require_POST)
def item_clear(request: HttpRequest, id: int):
    cart = Cart(request)
    cart.remove(product=Product.objects.filter(id=id).first())
    return JsonResponse({
        'product': Product.objects.get(id=id).toJSON(),
        "result": "ok",
        "amount": cart.get_sum_of("quantity")
    })


@require_POST
def remove_quant(request: HttpRequest, id: int, quantity: int):
    Cart(request).add(product=Product.objects.filter(id=id).first(), quantity=quantity, action="remove")
    return JsonResponse({"result": "ok"})


# @method_decorator(require_POST)
def update_quant(request: HttpRequest, id: int, value: int):
    cart = Cart(request)
    product = Product.objects.get(pk=id)
    cart.update_quant(product=product, value=value)
    # return redirect(reverse_lazy('index'))
    return JsonResponse({
        "result": "ok",
        'product': product.toJSON(),
        "amount": cart.session[CART_SESSION_ID].get(id, {"quantity": value})["quantity"],
        'price': f'{product.price}'
    })


@require_POST
def remove(request: HttpRequest, id: int):
    Cart(request).decrement(product=Product.objects.filter(id=id).first())
    return JsonResponse({"result": "ok"})


@require_POST
def cart_pop(request: HttpRequest, ):
    cart = Cart(request)
    cart.pop()
    return JsonResponse({
        "result": "ok",
        "amount": cart.get_sum_of("quantity")
    })


@require_POST
def add_quant(request: HttpRequest, id: int, quantity: int):
    cart = Cart(request)
    cart.add(Product.objects.filter(id=id).first(), quantity)
    return JsonResponse({"result": "ok",
                         'product': Product.objects.get(id=id).toJSON(),
                         "amount": cart.session[CART_SESSION_ID].get(id, {"quantity": quantity})["quantity"]
                         })
