import pygame
import pytest

from shot import WEAPONS, Shot


@pytest.fixture
def shots():
    return pygame.sprite.Group()


@pytest.fixture(autouse=True)
def setup_shot_containers(shots):
    Shot.containers = (shots,)
    yield


def test_weapons_have_required_fields():
    required = {"shots", "spread_deg", "speed", "radius", "pierce", "cooldown", "color"}
    for name, cfg in WEAPONS.items():
        assert required <= cfg.keys(), f"weapon {name} missing fields"
    assert set(WEAPONS) == {"blaster", "spread", "lance"}


def test_lance_pierces_more_than_blaster():
    assert WEAPONS["lance"]["pierce"] > WEAPONS["blaster"]["pierce"]


def test_spread_fires_multiple_shots():
    assert WEAPONS["spread"]["shots"] > 1


def test_shot_moves_with_velocity():
    shot = Shot(0, 0, pygame.Vector2(100, 0))
    shot.update(0.1)
    assert shot.position.x == pytest.approx(10)


def test_shot_dies_off_screen(shots):
    shot = Shot(0, 360, pygame.Vector2(-1000, 0))
    shot.update(1.0)
    assert len(shots) == 0


def test_shot_draw_with_zero_velocity_does_not_crash():
    screen = pygame.Surface((100, 100))
    shot = Shot(50, 50, pygame.Vector2(0, 0))
    shot.velocity = pygame.Vector2(0, 0)
    shot.draw(screen)  # early return, no crash


def test_shot_draw_tracer_does_not_crash():
    screen = pygame.Surface((100, 100))
    shot = Shot(50, 50, pygame.Vector2(0, 500))
    shot.draw(screen)
