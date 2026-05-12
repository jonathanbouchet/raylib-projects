import pyray as pr

from solar_system.stellar_objects import Body, Planetoid, Star

def test_body_radius():
    star = Star(pr.Vector3(0, 0, 0), radius=2, color=pr.Color(252, 229, 112, 255)) 
    assert star.radius == 2


def test_missing_rgb_components():
    star = Star(pr.Vector3(0, 0, 0), radius=2, color=pr.Color(252, 229, 112)) 
    assert star.color.a == 255


def test_rgb_components():
    star = Star(pr.Vector3(0, 0, 0), radius=2, color=pr.Color(252, 229, 112, 255)) 
    assert star.color.r == 252