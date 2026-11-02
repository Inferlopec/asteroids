import sys
from pathlib import Path

import pytest

# Make the project root importable (game modules are not a package)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


@pytest.fixture(scope="session", autouse=True)
def pygame_setup():
    import os
    import pygame

    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    pygame.init()
    yield
    pygame.quit()
