import pygame
import pytest

from constants import (
    PLAYER_RADIUS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from player import Player
from shot import Shot
from particle import Particle


class FakeAsteroid:
    def __init__(self, x, y, radius):
        self.position = pygame.Vector2(x, y)
        self.radius = radius


@pytest.fixture
def player():
    group = pygame.sprite.Group()
    Player.containers = (group,)
    Shot.containers = (pygame.sprite.Group(),)
    Particle.containers = (pygame.sprite.Group(),)
    return Player(300, 300)


def test_ship_points_shape(player):
    points = player.ship_points()
    assert len(points) == 6
    # Nose is one radius ahead of the center
    nose = points[0]
    assert nose.distance_to(player.position) == pytest.approx(PLAYER_RADIUS)


def test_ship_points_rotate_with_player(player):
    player.rotation = 90
    points = player.ship_points()
    nose = points[0]
    # pygame rotates counter-clockwise, so at 90 deg the nose points left
    expected = player.position + pygame.Vector2(-PLAYER_RADIUS, 0)
    assert nose.distance_to(expected) < 1e-6


def test_collision_hit_ahead(player):
    assert player.collides_with_asteroid(FakeAsteroid(300, 290, 20))


def test_no_collision_far_away(player):
    assert not player.collides_with_asteroid(FakeAsteroid(600, 600, 20))


def test_blaster_shoots_single_shot(player):
    group = pygame.sprite.Group()
    Shot.containers = (group,)
    player.timer = 0
    player.shoot()
    assert len(group) == 1
    assert group.sprites()[0].pierce == 1


def test_spread_shoots_three_fanned_shots(player):
    group = pygame.sprite.Group()
    Shot.containers = (group,)
    player.weapon = "spread"
    player.timer = 0
    player.shoot()
    assert len(group) == 3
    velocities = [s.velocity for s in group]
    # The fan should produce three distinct directions
    assert len({round(v.x, 3) for v in velocities}) == 3
    # All shots keep the weapon speed
    assert all(v.length() == pytest.approx(500) for v in velocities)


def test_shoot_sets_cooldown(player):
    player.timer = 0
    player.shoot()
    assert player.timer == pytest.approx(0.3)


def test_respawn_resets_state(player):
    player.position = pygame.Vector2(10, 10)
    player.weapon = "lance"
    player.shield_timer = 5
    player.lives = 1
    player.respawn()
    assert player.position == pygame.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    assert player.weapon == "blaster"
    assert player.shield_timer == 0
    assert player.invincible_timer == pytest.approx(3.0)
    assert player.lives == 1  # respawn does not touch lives


def test_move_advances_along_forward(player):
    start = player.position.copy()
    player.move(0.1)
    assert player.position.distance_to(start) == pytest.approx(20)  # 200 px/s * 0.1
