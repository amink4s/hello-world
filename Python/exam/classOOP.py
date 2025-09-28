class BaseShape:
    def __init__(self, name, side_a, side_b):
        self.name = name
        self.side_a = side_a
        self.side_b = side_b
        self._area = 0
        self._perimeter = 0
        self._diagonal = 0
        self.is_square = False
        self.calculate_properties()
        self.check_square()
    def calculate_properties(self):
        self.area = self.side_a * self.side_b
        self.perimeter = 2 * (self.side_a + self.side_b)
        self.diagonal = (self.side_a**2 + self.side_b**2) ** 0.5
    def check_square(self):
        self.is_square = self.side_a == self.side_b
    def display_info(self):   
        print(f"Shape: {self.name}")
        print(f"Sides: {self.side_a}, {self.side_b}")
        print(f"Area: {self.area}")
        print(f"Perimeter: {self.perimeter}")
        print(f"Diagonal: {self.diagonal}")
        print(f"Is Square: {self.is_square}")
    def __str__(self):
        return (f"{self.name} Object | Sides: {self.side_a} x {self.side_b} | "
                f"Area: {self.area:.2f} | Perimeter: {self.perimeter:.2f}")
    
class Rectangle(BaseShape):
    def __init__(self, side_a, side_b, color):
        super().__init__("Rectangle", side_a, side_b)
        self.color = color 
    def display_info(self):
        super().display_info()
        print(f"Color: {self.color}")
    def __str__(self):
        return (f"{super().__str__()} | Color: {self.color}")

class Square(BaseShape):
    def __init__(self, side, color):
        super().__init__("Square", side, side)
        self.color = color
    def display_info(self):
        super().display_info()
        print(f"Color: {self.color}")
    def __str__(self):
        return (f"{super().__str__()} | Color: {self.color}")
    def change_color(self, new_color):
        self.color = new_color
