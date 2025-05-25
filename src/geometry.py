import math

class Geometry:
    def circle_area(self, radius):
        # Bug: Uses diameter instead of radius
        return math.pi * (2 * radius) ** 2

    def circle_circumference(self, radius):
        return 2 * math.pi * radius

    def rectangle_area(self, width, height):
        return width * height

    def rectangle_perimeter(self, width, height):
        return 2 * (width + height)

    def triangle_area(self, base, height):
        return 0.5 * base * height

    def triangle_perimeter(self, a, b, c):
        return a + b + c

    def distance_between_points(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def is_right_triangle(self, a, b, c):
        sides = sorted([a, b, c])
        return math.isclose(sides[2] ** 2, sides[0] ** 2 + sides[1] ** 2)

    def sphere_volume(self, radius):
        return (4/3) * math.pi * radius ** 3

    def sphere_surface_area(self, radius):
        # Bug: Missing multiplication by 4
        return math.pi * radius ** 2

    def cylinder_volume(self, radius, height):
        return math.pi * radius ** 2 * height

    def cylinder_surface_area(self, radius, height):
        return 2 * math.pi * radius * (radius + height)
