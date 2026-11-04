import pygame
import pytest

from bomb import Bomb
from constants import BOMB_RADIUS, SCREEN_WIDTH


@pytest.fixture
def bombs():
    return pygame.sprite.Group()


@pytest.fixture(autouse=True)
def setup_containers(bombs):
    Bomb.containers = (bombs,)
    yield


def test_bomb_has_expected_radius(bombs):
    b = Bomb(100, 100)
    assert b.radius == BOMB_RADIUS
    assert b.velocity.length() == 0


def test_bomb_moves_with_velocity(bombs):
    b = Bomb(100, 100)
    b.velocity = pygame.Vector2(100, 0)
    b.update(0.1)
    assert b.position.x == pytest.approx(110)


def test_bomb_kills_when_off_screen(bombs):
    b = Bomb(SCREEN_WIDTH + BOMB_RADIUS + 1, 100)
    b.update(0.01)
    assert len(bombs) == 0
