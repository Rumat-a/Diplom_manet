from Product import Product
from Discount import Discount
from Dimensions import Dimensions
print('_______________________________________________________\n')
name = input()
price = int(input())
length = int(input())
width = int(input())
height = int(input())

prod_2 = Product(name, price, length, width, height)
prod_3 = Product('Тыковка', 90, 25, 10, 15)
prod_1 = Product('Дынька', 100, 40, 20, 19)
prod_1.display_info()
prod_2.display_info()
prod_3.display_info()

print('________\n')

disc_1 = Discount(prod_1, 30)
disc_1.display_info()
print('Цена с учетом скидки - ', prod_1.result_price(disc_1))

print('________\n')

disc_2 = Discount(prod_2, 40)
disc_2.display_info()
print('Цена с учетом скидки - ', prod_2.result_price(disc_2))

print('________\n')

disc_3 = Discount(prod_3, 15)
disc_3.display_info()
print('Цена с учетом скидки - ', prod_3.result_price(disc_3))

print('________\n')

dimen_1 = Dimensions(prod_1, 400, 200, 220)
dimen_1.display_info()

print('________\n')

dimen_2 = Dimensions(prod_2, 70, 90, 120)
dimen_2.display_info()

print('________\n')

dimen_3 = Dimensions(prod_3, 4, 5, 20)
dimen_3.display_info()

print('________\n')

print('Сколько товара prod_1 поместится в кейсe diment_1 - ',
      prod_1.quantity_prod_in_case(dimen_1))

print('________\n')

print('Сколько товара prod_2 поместится в кейсe diment_2 - ',
      prod_2.quantity_prod_in_case(dimen_2))

print('________\n')

print('Сколько товара prod_3 поместится в кейсe diment_3 - ',
      prod_3.quantity_prod_in_case(dimen_3))

print('_______________________________________________________\n')
