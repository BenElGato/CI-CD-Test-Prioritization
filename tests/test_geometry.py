import math
import pytest
from src.geometry import Geometry

geo = Geometry()

def test_circle_area():
    r = 3
    expected = math.pi * r**2
    assert math.isclose(geo.circle_area(r), expected)

def test_circle_circumference():
    r = 4
    expected = 2 * math.pi * r
    assert math.isclose(geo.circle_circumference(r), expected)

def test_rectangle_area_and_perimeter():
    assert geo.rectangle_area(5, 6) == 30
    assert geo.rectangle_perimeter(5, 6) == 22

def test_triangle_area_and_perimeter():
    assert geo.triangle_area(10, 5) == 25
    assert geo.triangle_perimeter(3, 4, 5) == 12

def test_distance_between_points():
    assert math.isclose(geo.distance_between_points(0, 0, 3, 4), 5)

def test_is_right_triangle():
    assert geo.is_right_triangle(3, 4, 5)
    assert not geo.is_right_triangle(3, 4, 6)

def test_sphere_volume_and_surface_area():
    r = 2
    expected_volume = (4/3) * math.pi * r**3
    assert math.isclose(geo.sphere_volume(r), expected_volume)

    expected_surface_area = 4 * math.pi * r**2
    assert math.isclose(geo.sphere_surface_area(r), expected_surface_area)

def test_cylinder_volume_and_surface_area():
    r, h = 3, 5
    assert math.isclose(geo.cylinder_volume(r, h), math.pi * r**2 * h)
    assert math.isclose(geo.cylinder_surface_area(r, h), 2 * math.pi * r * (r + h))
