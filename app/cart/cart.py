import json
from decimal import Decimal

from django.conf import settings
from django.db.models import QuerySet, F

from orders.models import Order, OrderItem
from store.models import Product
from .services import messages


class Cart:

    def __init__(self, session):

        self.session = session
        if not self.session.get(settings.CART_SESSION_ID):
            self.session[settings.CART_SESSION_ID] = {}
        self.cart = self.session[settings.CART_SESSION_ID]
        self.sorted_cart = {}
        self.warning_messages = []

    def add(self, product: dict, quantity: int):
        """
        Add product to db
        :param product: format is
             {"slug":{
                    "name": str,
                    "price": str,
                    "total_price": str),
                    "photo": str
                    }
            }
        :type product: dict
        :param quantity:
        :type quantity: int
        """
        slug = [key for key in product][0]

        if slug not in self.cart:
            product[slug]['quantity'] = quantity
            self.cart |= product
            self.__set_total_product_price(slug, product)
        else:
            self.cart[slug]['quantity'] += quantity
            self.__set_total_product_price(slug, product)

        self.__save()

    def remove(self, slug: str):
        """
        Removing an item from the cart.
        """
        if slug in self.cart:
            del self.cart[slug]
            self.__save()

    def sort(self, slugs: list[str]):
        """
        Sorting cart according to product order in db
        """
        self.sorted_cart = self.__sort_help(self.cart, slugs)
        self.__save()

    def check_products_amount(self, products: QuerySet[Product]):
        for slug, product in zip(self.sorted_cart.copy(), products):
            if self.sorted_cart[slug]['quantity'] > product.amount:

                if not product.amount:
                    self.__product_is_over(product, slug)
                else:
                    self.__quantity_is_less_then_possible_amount(product, slug)

        self.cart = self.__sort_help(self.sorted_cart, list(self.cart.keys()))
        self.__save()

    def create_order_items(self, order: Order, products: QuerySet[Product]):
        self.check_products_amount(products)

        if not self.warning_messages:
            for slug, product in zip(self.sorted_cart.copy(), products):
                quantity = self.sorted_cart[slug]['quantity']

                OrderItem.objects.create(
                    order=order, product=product, quantity=quantity)

                product.amount = F('amount') - quantity

                product.save(update_fields=['amount'])
                self.__clear()
            return True
        else:
            return False

    def get_total_sum(self):
        """
        Calculate the cost of all items in the shopping cart.
        """
        return sum(Decimal(self.cart[i]['total']) for i in self.cart)

    def __clear(self):
        """
        Delete cart from session
        """
        self.cart = {}
        self.__save()

    def __save(self):
        """
        Cart session update
        """
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    @staticmethod
    def __sort_help(dict_: dict, list_: list) -> dict:
        """
        Sorting a dict_ according to list_
        Example:
        >>> d={\
        'main_key2': {'key': 'value'},\
        'main_key1': {'key': 'value'}\
        }
        >>> l = ["main_key2", "main_key1"]
        >>> __sort_help(d, l)
        {'main_key2': {'key': 'value'}, 'main_key1': {'key': 'value'}}

        """
        return dict(sorted(dict_.items(),
                           key=lambda item: list_.index(item[0])))

    def __set_total_product_price(self, slug: str, product: dict,
                                  is_sorted: bool = False):

        cart = self.cart if not is_sorted else self.sorted_cart

        cart[slug]['total'] = str(cart[slug]['quantity'] * Decimal(
            product[slug]['total_price']))

    def __product_is_over(self, product: Product, slug: str):
        msg = messages.PRODUCT_IS_OVER.format(product=product)
        self.warning_messages.append(msg)
        del self.sorted_cart[slug]

    def __quantity_is_less_then_possible_amount(self, product: Product,
                                                slug: str):
        msg = messages.QUANTITY_IS_LESS_THEN_POSSIBLE_AMOUNT.format(
            quan=self.cart[slug]['quantity'], product=product,
            amount=product.amount)
        self.warning_messages.append(msg)
        self.sorted_cart[slug]['quantity'] = product.amount
        self.__set_total_product_price(
            slug, json.loads(product.as_cart_item()), True)