from Product import Product


class Discount(Product):
    def __init__(self, product, discount_quantity_):
        Product.__init__(self, product.name_prod, product.price_prod, product.length_prod, product.width_prod, product.height_prod)
        self.discount_quantity = discount_quantity_

    @classmethod
    def verify_discount(cls, discount):
        if discount <= 0 or discount >= 100:
            raise ValueError('Скидка дожна быть в пределах (0:100)%')

    # Определение Геттера и Сеттера
    @property
    def discount_quantity(self):
        return self.__discount_quantity

    @discount_quantity.setter
    def discount_quantity(self, discount_quantity):
        self.verify_discount(discount_quantity)
        self.__discount_quantity = discount_quantity

    def __str__(self):
        return "\nDiscount: {}% \n".format(self.__discount_quantity) + Product.__str__(self)

    def display_info(self):
        print(self.__str__())
