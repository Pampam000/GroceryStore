from decimal import Decimal

from django.conf import settings

from store.models import Product


class Cart:

    def __init__(self, session):

        self.session = session
        if not self.session.get(settings.CART_SESSION_ID):
            self.session[settings.CART_SESSION_ID] = {}
        self.cart = self.session[settings.CART_SESSION_ID]

        self.iter = 0
        self.products = []

    def __iter__(self):
        """
        Iterating through the items in the cart and getting the products from
        the database.
        """

        product_ids = self.cart.keys()
        # getting product objects and adding them to cart
        self.products = Product.objects.filter(
            id__in=product_ids).select_related(
            'producer')
        return self

    def __next__(self):

        if self.iter >= len(self.products):
            self.iter = 0
            self.products = []
            raise StopIteration
        else:
            product = self.products[self.iter]
            self.cart[str(product.pk)]['product'] = product
            item = list(self.cart.values())[self.iter]
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            self.iter += 1
            return item

    def __len__(self):
        """
        Counting all items in the cart.
        """

        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product: Product, quantity: int = 1):
        """
        Add product to cart
        """
        product_id = str(product.pk)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.total_price())}

        self.cart[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        """
        Cart session update
        """

        self.session[settings.CART_SESSION_ID] = self.cart

        # Mark session as "modified" to make sure it's saved
        self.session.modified = True

    def remove(self, product: Product, save: bool = True):
        """
           Removing an item from the cart.
        """

        product_id = str(product.pk)
        if product_id in self.cart:
            del self.cart[product_id]
            if save:
                self.save()

    def get_total_price(self):
        """
        Calculate the cost of items in the shopping cart.
        """
        return sum(self.get_item_total_price(item) for item in
                   self.cart.values())

    def clear(self):
        """
        Delete cart from session
        """
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    @staticmethod
    def get_item_total_price(item: dict):
        return Decimal(item['price']) * item['quantity']
