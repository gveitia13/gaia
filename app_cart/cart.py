from django.core.cache import cache


class Wrapper(dict):
    def __init__(self, model) -> None:
        self.__dict__ = model.__dict__
        del self.__dict__["_state"]
        super().__init__(model.__dict__)


class Cart(object):
    def __init__(self, request=None):
        if request is not None:
            self.request = request
            self.session = request.headers.get('X-Session-ID')

    def add(self, product, quantity=1):
        """
        Add a product to the cart or update its quantity.
        """
        q = int(quantity)
        stock = int(product.stock)
        shopping_cart = cache.get(self.session) or {}
        if str(product.id) not in shopping_cart:
            shopping_cart[str(product.id)] = q if q <= stock else stock
        else:
            amount = int(cache.get(self.session)[str(product.id)])
            shopping_cart[str(product.id)] = amount + q if (amount + q) <= stock else stock
        self.save(shopping_cart)


    def subtract(self, product, quantity=1):
        """
        Subtract a product from the cart or update its quantity.
        """
        q = int(quantity)
        shopping_cart = cache.get(self.session) or {}
        if str(product.id) in shopping_cart:
            amount = int(cache.get(self.session)[str(product.id)])
            new_quantity = max(amount - q, 0)
            if new_quantity == 0:
                del shopping_cart[str(product.id)]
            else:
                shopping_cart[str(product.id)] = new_quantity
            self.save(shopping_cart)

    def save(self, shopping_cart):
        # update the session cart
        cache.set(self.session, shopping_cart, 60 * 60 * 4)

    def get(self, id):
        if str(id) in cache.get(self.session):
            return cache.get(self.session)[str(id)]
        else:
            return 0

    def all(self):
        return list(cache.get(self.session).keys())

    def set(self, key, value):
        cache.get(self.session)[str(key)] = value

    def get_sum_of(self, key):
        return sum(map(lambda x: float(x), cache.get(self.session).values()))

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        cart = cache.get(self.session)
        if str(product.id) in cart:
            del cart[str(product.id)]
            cache.set(self.session, cart)

    def pop(self):
        if len(cache.get(self.session)) > 0:
            last_product = list(cache.get(self.session).values()).pop()
            del cache.get(self.session)[str(last_product['id'])]

    def decrement(self, product):
        if str(product.id) in cache.get(self.session):
            new_quantity = int(cache.get(self.session)[str(product.id)]) - 1
            if new_quantity < 1:
                del cache.get(self.session)[str(product.id)]
            else:
                cache.get(self.session)[str(product.id)] = new_quantity

    # mio
    def update_quant(self, product, value):
        q = int(value)
        stock = int(product.stock)
        if str(product.id) in cache.get(self.session):
            if q >= stock:
                new_quantity = stock
            else:
                new_quantity = q
            cache.get(self.session)[str(product.id)] = new_quantity

    def clear(self):
        # empty cart
        cart = cache.get(self.session)
        for product_id in list(cart.keys()):
            del cart[str(product_id)]
        cache.set(self.session, cart)
