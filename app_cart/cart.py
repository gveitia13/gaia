import json
from django.conf import settings
from django.shortcuts import redirect

from app_main.models import Product


class Wrapper(dict):
    def __init__(self, model) -> None:
        self.__dict__ = model.__dict__
        del self.__dict__["_state"]
        super().__init__(model.__dict__)


class Cart(object):
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:  # or True:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        """
        Add a product to the cart its quantity.
        """
        if str(product.id) not in self.cart.keys():
            self.cart[str(product.id)] = {
                "id": str(product.id),
                'user_id': self.request.user.id,
                # "product": Wrapper(product),
                'product': product.toJSON(),
                'quantity': int(quantity)
            }
            print(self.cart[str(product.id)])
        else:
            self.cart[str(product.id)]['quantity'] = int(self.cart[str(product.id)]['quantity']) + int(quantity)
            print(self.cart[str(product.id)])
        self.save()

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def get(self, id):
        return self.session[settings.CART_SESSION_ID][id]

    def all(self, ):
        return list(self.session[settings.CART_SESSION_ID].values())

    def set(self, key, value):
        self.cart[key] = value
        self.save()

    def update(self, key, content: dict):
        for k in content.keys():
            self.cart[k][key] = content[k]
        self.save()

    def clear_garbage(self, key, value):
        for i in self.all():
            if i[key] == value:
                del self.cart[i["id"]]
        self.save()

    def get_sum_of(self, key):
        return sum(map(lambda x: float(x[key]), self.all()))

    def get_multiply_of(self, key1, key2):
        return map(lambda x: float(x[key1]) * float(x[key2]), self.all())

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        if str(product.id) in self.cart:
            del self.cart[str(product.id)]
            self.save()

    def pop(self, ):
        del self.session[settings.CART_SESSION_ID][str(self.all().pop()['id'])]
        self.save()

    def decrement(self, product):
        self.cart[str(product.id)]['quantity'] = int(self.cart[str(product.id)]['quantity']) - 1
        if self.cart[str(product.id)]['quantity'] < 1:
            return redirect('cart:cart_detail')
        self.save()

    # mio
    def update_quant(self, product, value):
        self.cart[str(product.id)]['quantity'] = int(value)
        self.save()
        # if str(product.id) not in self.cart.keys():
        #     self.cart[str(product.id)] = {
        #         "id": str(product.id),
        #         'user_id': self.request.user.id,
        #         'product': product.toJSON(),
        #         'quantity': int(value)
        #     }
        #     print(self.cart[str(product.id)])
        # else:
        #     self.cart[str(product.id)]['quantity'] = int(value)
        #     print(self.cart[str(product.id)])
        # self.save()

    def clear(self):
        # empty cart
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True
