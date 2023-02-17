from typing import NamedTuple

from cart.cart import Cart
from . import messages as msgs


class CartChecker(NamedTuple):
    cart: Cart
    messages: list = []
    products_to_remove: list = []

    def check_cart_items_in_db(self):

        for item in self.cart:
            if item['quantity'] > item['product'].amount:
                self.__check_amount(item)

        for product in self.products_to_remove:
            del self.cart.cart[str(product.pk)]

        return self

    def __check_amount(self, item: dict):

        if not item['product'].amount:
            msg = msgs.PRODUCT_IS_OVER.format(product=item['product'])
            if msg not in self.messages:
                self.messages.append(msg)
            if item['product'] not in self.products_to_remove:
                self.products_to_remove.append(item['product'])
        else:
            msg = msgs.QUANTITY_IS_LESS_THEN_POSSIBLE_AMOUNT.format(
                quan=item['quantity'], product=item['product'],
                amount=item['product'].amount)
            if msg not in self.messages:
                self.messages.append(msg)
            self.__update_item(item)

    def __update_item(self, item: dict):
        item['quantity'] = item['product'].amount
        item['total_price'] = self.cart.get_item_total_price(item)
