from django.http import HttpRequest, JsonResponse
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
    print(str(cart))
    cart.add(product=Product.objects.filter(id=id).first())
    return JsonResponse({
        'product': f'{id} {Product.objects.get(id=id).name}',
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
        'product': f'{id} {Product.objects.get(id=id).name}',
        "result": "ok",
        "amount": cart.get_sum_of("quantity")
    })


@require_POST
def remove_quant(request: HttpRequest, id: int, quantity: int):
    Cart(request).add(product=Product.objects.filter(id=id).first(), quantity=quantity, action="remove")
    return JsonResponse({"result": "ok"})


@method_decorator(require_POST)
def update_quant(request: HttpRequest, id: int, value: int):
    cart = Cart(request)
    product = Product.objects.get(pk=id)
    cart.update_quant(product=product, value=value)
    return JsonResponse({
        "result": "ok",
        'product': f'{id} {product.name}',
        "amount": cart.session[CART_SESSION_ID].get(id, {"quantity": value})["quantity"],
        'price': f'{product.price}'
    })


# @method_decorator(csrf_exempt, require_POST)
# def clear_current_cart(request: HttpRequest, id: int, ):
#     cart = Cart(request)
#     ids = request.session[settings.CART_SESSION_ID]
#     user = GeneralData.objects.get(pk=id).user
#     for p in Product.objects.filter(user_id=user.pk):
#         for i in ids:
#             if str(p.pk) == i:
#                 cart.remove(p)


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
                         'product': f'{id} {Product.objects.get(id=id).name}',
                         "amount": cart.session[CART_SESSION_ID].get(id, {"quantity": quantity})["quantity"]
                         })
