import pygame
import pytest

from constants import (
    BOMB_COUNT,
    PLAYER_ACCELERATION,
    PLAYER_MAX_SPEED,
    PLAYER_RADIUS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SPEED_DURATION,
    SPEED_MULTIPLIER,
)
from bomb import Bomb
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
    player.speed_timer = 5
    player.bombs = 0
    player.lives = 1
    player.respawn()
    assert player.position == pygame.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    assert player.weapon == "blaster"
    assert player.shield_timer == 0
    assert player.speed_timer == 0
    assert player.bombs == BOMB_COUNT
    assert player.invincible_timer == pytest.approx(3.0)
    assert player.lives == 1  # respawn does not touch lives


def test_move_accelerates_along_forward(player):
    player.move(0.1)
    # move() applies acceleration, not direct velocity
    assert player.velocity.length() == pytest.approx(PLAYER_ACCELERATION * 0.1)
    assert player.velocity.y == pytest.approx(PLAYER_ACCELERATION * 0.1)


def test_update_advances_position_by_velocity(player, monkeypatch):
    _set_input(monkeypatch)
    start = player.position.copy()
    player.velocity = pygame.Vector2(0, 100)
    player.update(0.1)
    assert player.position.distance_to(start) == pytest.approx(10)


def test_speed_pickup_boosts_max_speed(player, monkeypatch):
    _set_input(monkeypatch)
    player.speed_timer = SPEED_DURATION
    player.velocity = pygame.Vector2(0, 1000)
    player.update(0.016)
    assert player.velocity.length() == pytest.approx(PLAYER_MAX_SPEED * SPEED_MULTIPLIER)


def test_drop_bomb_spawns_bomb(player):
    group = pygame.sprite.Group()
    Bomb.containers = (group,)
    player.bombs = 1
    player.drop_bomb()
    assert len(group) == 1
    assert player.bombs == 0


def test_drop_bomb_noop_when_empty(player):
    group = pygame.sprite.Group()
    Bomb.containers = (group,)
    player.bombs = 0
    player.drop_bomb()
    assert len(group) == 0
    assert player.bombs == 0


class FakeKeys:
    """Stand-in for pygame.key.get_pressed() with a chosen set of held keys."""
    def __init__(self, *pressed):
        self.pressed = set(pressed)

    def __getitem__(self, key):
        return key in self.pressed


def _set_input(monkeypatch, keys=(), left_mouse=False):
    monkeypatch.setattr(pygame.key, "get_pressed", lambda: FakeKeys(*keys))
    monkeypatch.setattr(pygame.mouse, "get_pressed", lambda *a, **k: (left_mouse, False, False))


def test_left_mouse_click_fires(player, monkeypatch):
    _set_input(monkeypatch, left_mouse=True)
    player.update(0.016)
    assert len(Shot.containers[0]) == 1
    assert player.timer > 0


def test_space_still_fires(player, monkeypatch):
    _set_input(monkeypatch, keys=(pygame.K_SPACE,))
    player.update(0.016)
    assert len(Shot.containers[0]) == 1


def test_no_input_does_not_fire(player, monkeypatch):
    _set_input(monkeypatch)
    player.update(0.016)
    assert len(Shot.containers[0]) == 0


def test_mouse_fire_respects_cooldown(player, monkeypatch):
    _set_input(monkeypatch, left_mouse=True)
    player.update(0.016)
    player.update(0.016)
    assert len(Shot.containers[0]) == 1
