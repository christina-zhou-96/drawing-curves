from car import *

my_car = car.Car('yellow', 'beetle',1967)
my_other_car = car.Car('red','corvette',1999)
print(f"My care is {my_car.color}")

print(f'it had {my_car.wheels} wheels')

print(f'my other car is {my_other_car.color}')
print(f'it has {my_other_car.wheels} wheels')

car.Car.wheels = 4
my_car.wheels = 5