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
from django.core.cache import cache


# @require_POST
@method_decorator(csrf_exempt, require_POST)
def add(request: HttpRequest, id: int):
    cart = Cart(request)
    product = Product.objects.filter(id=id).first()
    cart.add(product=product)
    return JsonResponse({
        'product': product.toJSON(),
        "result": "ok",
        "amount": cache.get(cart.session)[str(product.id)]
    })


@method_decorator(csrf_exempt, require_POST)
def cart_detail(request: HttpRequest, id: int):
    cart = Cart(request)
    item = cart.get(id)

    return JsonResponse({"result": item})





# @require_POST
@method_decorator(csrf_exempt, require_POST)
def remove_quant(request: HttpRequest, id: int, quantity: int):
    Cart(request).add(product=Product.objects.filter(id=id).first(), quantity=quantity, action="remove")
    return JsonResponse({"result": "ok"})


# @method_decorator(require_POST)
@method_decorator(csrf_exempt, require_POST)
def update_quant(request: HttpRequest, id: int, value: int):
    cart = Cart(request)
    product = Product.objects.get(pk=id)
    cart.update_quant(product=product, value=value)
    return JsonResponse({
        "result": "ok",
        'product': product.toJSON(),
        "amount": cart.session[CART_SESSION_ID].get(id, {"quantity": value})["quantity"],
        'price': f'{product.price}'
    })


# @method_decorator(require_POST)
@method_decorator(csrf_exempt, require_POST)
def update_quant_bl(request: HttpRequest, id: int, value: int):
    cart = Cart(request)
    product = Product.objects.get(pk=id)
    cart.update_quant(product=product, value=value)
    total = 0
    for item in cart.session[CART_SESSION_ID]:
        total = total + (cart.session[CART_SESSION_ID].get(item)['product']['price'] *
                         cart.session[CART_SESSION_ID].get(item)['quantity'])
    return JsonResponse({
        "result": "ok",
        "total": total,
        'product': product.toJSON(),
        "amount": cart.session[CART_SESSION_ID].get(id, {"quantity": value})["quantity"],
        'price': f'{product.price}'
    })


# @require_POST
@method_decorator(csrf_exempt, require_POST)
def remove(request: HttpRequest, id: int):
    Cart(request).decrement(product=Product.objects.filter(id=id).first())
    request.session['active'] = '2'
    return JsonResponse({"result": "ok"})


# @require_POST
@method_decorator(csrf_exempt, require_POST)
def cart_pop(request: HttpRequest, ):
    cart = Cart(request)
    cart.pop()
    request.session['active'] = '2'
    return JsonResponse({
        "result": "ok",
        "amount": cart.get_sum_of("quantity")
    })


# @require_POST
@method_decorator(csrf_exempt, require_POST)
def add_quant(request: HttpRequest, id: int, quantity: int):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product, quantity)
    return JsonResponse({
        'product': product.toJSON(),
        "result": "ok",
        "amount": cache.get(cart.session)[str(product.id)]
    })

@method_decorator(csrf_exempt, require_POST)
def decrement_quant(request: HttpRequest, id: int, quantity: int):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.subtract(product, quantity)
    return JsonResponse({
        'product': product.toJSON(),
        "result": "ok",
        "amount": cache.get(cart.session)[str(product.id)]
    })

@method_decorator(csrf_exempt, require_POST)
def item_clear(request: HttpRequest, id: int):
    try:
        cart = Cart(request)
        product = Product.objects.get(pk=id)
        cart.remove(product=product)
        return JsonResponse({
            'product': product.toJSON(),
            "result": "ok",
            "amount": cart.get_sum_of("quantity")
        })
    except:
        return JsonResponse({
            "status": 403,
            "result": "ko",
        })

@method_decorator(csrf_exempt, require_POST)
def cart_clear(request: HttpRequest):
    Cart(request).clear()
    return JsonResponse({
        'product': None,
        "result": "ok",
        "amount": 0
    })
