import pygame

from circleshape import CircleShape


def make(x, y, radius):
    return CircleShape(x, y, radius)


def test_initial_state():
    c = make(10, 20, 30)
    assert c.position == pygame.Vector2(10, 20)
    assert c.velocity == pygame.Vector2(0, 0)
    assert c.radius == 30


def test_collides_when_overlapping():
    assert make(0, 0, 10).collides_with(make(15, 0, 10))


def test_no_collision_when_separate():
    assert not make(0, 0, 10).collides_with(make(50, 0, 10))


def test_touching_circles_do_not_collide():
    # collides_with uses strict <, so exact tangency is not a collision
    assert not make(0, 0, 10).collides_with(make(20, 0, 10))
