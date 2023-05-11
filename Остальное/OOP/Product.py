import math


class Product:

    # Прописывем параметры объекта класса
    def __init__(self, name_prod_, price_prod_, length_prod_, width_prod_, height_prod_):
        # Тут вызывается не создается переменная __name, тут вызывается setter name, т.к он определен ниже, так же и для остальных переменных, для кого определен сеттер
        self.name_prod = name_prod_
        self.price_prod = price_prod_
        self.length_prod = length_prod_
        self.width_prod = width_prod_
        self.height_prod = height_prod_

    # Методы для верификации вводимых параметров

    @classmethod
    def verify__price(cls, price):
        if price < 0.01:
            # Вызовет оштбку при неправильном значении цены
            raise ValueError('Минимальная цена 0.01руб')

    # За параметры максимальных габаритов взяты внутренние размеры морского сухогрузного контейнера - 20 футов
    @classmethod
    def verify__length(cls, length):
        if length <= 0 or length > 590.5:
            raise ValueError(
                'Длинна продукта/кейса может быть в приделах (0:590.5]см')

    @classmethod
    def verify_width(cls, width):
        if width <= 0 or width > 235.2:
            raise ValueError(
                'Ширина продукта/кейса может быть в приделах (0:235.2]см')

    @classmethod
    def verify_hiegth(cls, hiegth):
        if hiegth <= 0 or hiegth > 239.3:
            raise ValueError(
                'Высота продукта/кейса может быть в приделах (0:239.3]см')

    # Т.к переменные объекта приватные, к ним нужно обращаться через геттер и сеттер
    # Геттеры:

    @property
    def name_prod(self):
        return self.__name_prod

    @name_prod.setter
    def name_prod(self, name_prod):
        self.__name_prod = name_prod

    @property
    def price_prod(self):
        return self.__price_prod

    @price_prod.setter
    def price_prod(self, price_prod):
        # Вызовет оштбку при неправильном значении цены
        self.verify__price(price_prod)
        self.__price_prod = price_prod

    @property
    def length_prod(self):
        return self.__length_prod

    @length_prod.setter
    def length_prod(self, length_prod):
        self.verify__length(length_prod)
        self.__length_prod = length_prod

    @property
    def width_prod(self):
        return self.__width_prod

    @width_prod.setter
    def width_prod(self, width_prod):
        self.verify_width(width_prod)
        self.__width_prod = width_prod

    @property
    def height_prod(self):
        return self.__height_prod

    @height_prod.setter
    def height_prod(self, height_prod):
        self.verify_hiegth(height_prod)
        self.__height_prod = height_prod

    # Посте добавления возможности обращения к переменным объекта и их изменения
    # остается добавить возможность корректного отображения объекта

    def __str__(self):
        return "Product: name_prod: {}   price_prod: {}   length: {}   width: {}   height: {}".format(
            self.name_prod,
            self.price_prod,
            self.length_prod,
            self.width_prod,
            self.height_prod
        )

    def display_info(self):
        print(self.__str__())

    # После добавления переменных объета и дефолтных методов добавим методы для:
    # высчиывания цены с учетом скидки
    # высчитывает, сколько товара определенных габаритов может поместиться в коробку, тоже определенных габаритов

    def quantity_prod_in_case(self, dimensions):
        self.verify__length(dimensions.length_case)
        self.verify_hiegth(dimensions.height_case)
        self.verify_width(dimensions.width_case)
        return math.floor(dimensions.width_case * dimensions.height_case * dimensions.length_case / (self.width_prod * self.height_prod * self.length_prod))

    def result_price(self, discount):
        result_price = self.__price_prod * \
            (1 - discount.discount_quantity / 100)
        if result_price < 0.01:
            return 0.01
        else:
            return float('{:.2f}'.format(result_price))
