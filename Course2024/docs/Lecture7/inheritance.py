# Inheritance = Allows a class to inherit attributes and methods from another class
#               Helps with code resuability and extensibility
#               class Child(Parent) aka sub(super)


class Animal:
    def __init__(self, name):
        self.name = name
        self.is_alive = True
    
    def eat(self):
        print(f"{self.name} is eating")

    def sleep(self):
        print(f"{self.name} is sleeping")

class Dog(Animal):
    pass

class Cat(Animal):
    pass

class Mouse(Animal):
    pass

dog = Dog("Scooby")
cat = Cat("Garfield")
mouse = Mouse("Mickey")


print(dog.name)
print(dog.is_alive)