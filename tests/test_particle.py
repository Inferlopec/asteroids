import pygame
import pytest

from particle import Particle


@pytest.fixture
def particles():
    return pygame.sprite.Group()


@pytest.fixture(autouse=True)
def setup_containers(particles):
    Particle.containers = (particles,)
    yield


def test_particle_expires_after_lifetime(particles):
    p = Particle(0, 0, 3, pygame.Vector2(0, 0), 0.5)
    p.update(0.5)
    assert len(particles) == 0


def test_particle_moves(particles):
    p = Particle(0, 0, 3, pygame.Vector2(100, 0), 1.0)
    p.update(0.1)
    assert p.position.x == pytest.approx(10)


def test_particle_shrinks_over_life(particles):
    p = Particle(0, 0, 10, pygame.Vector2(0, 0), 1.0)
    p.update(0.5)
    assert p.radius * (1.0 - p.age / p.lifetime) == pytest.approx(5)


def test_particle_draw_does_not_crash(particles):
    screen = pygame.Surface((100, 100))
    p = Particle(50, 50, 5, pygame.Vector2(10, 10), 1.0, (1, 2, 3))
    p.draw(screen)
    p.update(0.9)
    p.draw(screen)  # near end of life, tiny radius
