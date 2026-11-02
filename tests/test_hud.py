import pytest

from constants import SCORE_LARGE, SCORE_MEDIUM, SCORE_SMALL
from hud import HUD


@pytest.fixture
def hud():
    h = HUD()
    # Isolate from the real high_score.txt so tests are deterministic
    h.high_score = 0
    return h


def test_calculate_score_by_size(hud):
    assert hud.calculate_score(20) == SCORE_SMALL
    assert hud.calculate_score(40) == SCORE_MEDIUM
    assert hud.calculate_score(60) == SCORE_LARGE


def test_small_asteroids_score_more(hud):
    assert hud.calculate_score(20) > hud.calculate_score(40) > hud.calculate_score(60)


def test_update_score_accumulates_and_tracks_high_score(hud):
    hud.update_score(50)
    hud.update_score(60)
    assert hud.score == 110
    assert hud.high_score == 110


def test_reset_clears_score_not_high_score(hud):
    hud.update_score(100)
    hud.reset()
    assert hud.score == 0
    assert hud.high_score == 100
