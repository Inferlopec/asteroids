import random

import pygame
import pytest

from asteroid import Asteroid
from constants import ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS
from particle import Particle, spawn_explosion


@pytest.fixture
def asteroids():
    return pygame.sprite.Group()


@pytest.fixture(autouse=True)
def setup_containers(asteroids):
    Asteroid.containers = (asteroids,)
    Particle.containers = ()
    yield


def test_large_asteroid_splits_into_two_smaller(asteroids):
    a = Asteroid(300, 300, 60)
    a.split()
    children = [x for x in asteroids if x is not a]
    assert len(children) == 2
    assert all(c.radius == 40 for c in children)


def test_small_asteroid_does_not_split(asteroids):
    a = Asteroid(300, 300, ASTEROID_MIN_RADIUS)
    a.split()
    assert len(asteroids) == 0


def test_split_children_inherit_position(asteroids):
    a = Asteroid(300, 300, 60)
    a.split()
    children = [x for x in asteroids if x is not a]
    assert all(c.position == a.position for c in children)


def test_spawn_explosion_count_scales_with_radius():
    random.seed(1)
    group = pygame.sprite.Group()
    Particle.containers = (group,)
    spawn_explosion(pygame.Vector2(100, 100), pygame.Vector2(0, 0), ASTEROID_MAX_RADIUS)
    large = len(group)
    group = pygame.sprite.Group()
    Particle.containers = (group,)
    spawn_explosion(pygame.Vector2(100, 100), pygame.Vector2(0, 0), ASTEROID_MIN_RADIUS)
    small = len(group)
    assert large > small
