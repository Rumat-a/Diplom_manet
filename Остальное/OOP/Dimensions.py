from Product import Product


class Dimensions(Product):

    def __init__(self, product, length_case, width_case, height_case):
        Product.__init__(self, product.name_prod, product.price_prod,
                         product.length_prod, product.width_prod, product.height_prod)
        self.length_case = length_case
        self.width_case = width_case
        self.height_case = height_case

    # Определение сеттеров и геттеров
    # getter
    @property
    def length_case(self):
        return self.__length_case
    # setter
    @length_case.setter
    def length_case(self, length_case):
        self.verify__length(length_case)
        self.__length_case = length_case

    @property
    def width_case(self):
        return self.__width_case

    @width_case.setter
    def width_case(self, wigth_case):
        self.verify_width(wigth_case)
        self.__width_case = wigth_case

    @property
    def height_case(self):
        return self.__height_case

    @height_case.setter
    def height_case(self, height_case):
        self.verify_hiegth(height_case)
        self.__height_case = height_case

    def __str__(self):
        return 'Габариты кейса:  length: {}   width: {}   height: {}'.format(
            self.length_case,
            self.width_case,
            self.height_case
        )

    def display_info(self):
        print(self.__str__())
