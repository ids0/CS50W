# n = int(input("Enter a number:\t"))
n = 0
text = ""
if (n % 3 == 0):
    text = "foo"
if (n % 5 == 0):
    text += "bar"

print(text)

coordinate = {"x":5,"y":7}


class Point:

    def __init__(self, x,y):
        self.x = int(x)
        self.y = int(y)

    def __len__(self):
        return (self.x)

origin = Point(0,0)
p1 = Point(4,3)


class Polygon(object):
    def __init__(self,sides):
        self.number_of_sides = sides

    def number_of_sides(self):
        print(f"It has {self.sides} sides")

    def change_sides_lenght(self, *args):
        if len(args) == self.number_of_sides:
            self.sides_lenght = args
        else:
            print("Not the correct number of sides")
            self.sides_lenght = ()


triangle = Polygon(3)
triangle.change_sides_lenght(5,4,6,4)
print(triangle.sides_lenght)


