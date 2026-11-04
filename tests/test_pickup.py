import pygame
import pytest

from constants import (
    LIFE_PICKUP_COLOR,
    PICKUP_LIFETIME,
    PLAYER_MAX_LIVES,
    SCREEN_WIDTH,
    SHIELD_COLOR,
    SHIELD_DURATION,
    SPEED_COLOR,
    SPEED_DURATION,
)
from pickup import Pickup
from player import Player
from shot import WEAPONS


@pytest.fixture
def pickups():
    return pygame.sprite.Group()


@pytest.fixture(autouse=True)
def setup_containers(pickups):
    Pickup.containers = (pickups,)
    yield


def make_player():
    Player.containers = ()
    return Player(300, 300)


def test_shield_pickup_applies_duration(pickups):
    p = make_player()
    pk = Pickup(100, 100, "shield")
    pk.apply(p)
    assert p.shield_timer == pytest.approx(SHIELD_DURATION)
    assert pk.color == SHIELD_COLOR
    assert pk.label == "S"


def test_speed_pickup_applies_duration(pickups):
    p = make_player()
    pk = Pickup(100, 100, "speed")
    pk.apply(p)
    assert p.speed_timer == pytest.approx(SPEED_DURATION)
    assert pk.color == SPEED_COLOR
    assert pk.label == "F"


def test_life_pickup_restores_life(pickups):
    p = make_player()
    p.lives = 2
    pk = Pickup(100, 100, "life")
    pk.apply(p)
    assert p.lives == 3
    assert pk.color == LIFE_PICKUP_COLOR


def test_life_pickup_caps_at_max(pickups):
    p = make_player()
    p.lives = PLAYER_MAX_LIVES
    Pickup(100, 100, "life").apply(p)
    assert p.lives == PLAYER_MAX_LIVES


def test_weapon_pickup_equips_weapon(pickups):
    p = make_player()
    pk = Pickup(100, 100, "weapon", "lance")
    pk.apply(p)
    assert p.weapon == "lance"
    assert pk.color == WEAPONS["lance"]["color"]


def test_pickup_expires_after_lifetime(pickups):
    pk = Pickup(100, 100, "shield")
    pk.update(PICKUP_LIFETIME)
    assert len(pickups) == 0


def test_pickup_wraps_around_screen(pickups):
    pk = Pickup(-5, 300, "shield")
    pk.velocity = pygame.Vector2(-100, 0)
    pk.update(0.1)  # x goes past -radius, wrapping to the right edge
    assert pk.position.x > SCREEN_WIDTH


def test_spawn_weapon_never_returns_blaster(pickups):
    for _ in range(20):
        pk = Pickup.spawn("weapon", 100, 100)
        assert pk.kind == "weapon"
        assert pk.weapon in {"spread", "lance"}


def test_spawn_shield_and_life(pickups):
    assert Pickup.spawn("shield", 100, 100).kind == "shield"
    assert Pickup.spawn("life", 100, 100).kind == "life"
