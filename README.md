# asteroids

A classic Asteroids clone built with Python and pygame. Pilot an arrow-shaped
ship, blast lumpy asteroids into smaller pieces, and survive as long as you can.

Current version: 1.4.0

## Features

- Scoring system (small asteroids are worth more) with a persistent high score
- Multiple lives with respawn and a brief invincibility window
- Lumpy, rotating asteroids that split into two smaller ones when hit
- Particle explosion effect when asteroids are destroyed (scales with size)
- Arrow-shaped ship with a polygonal hit box (fairer than a circle)
- Asteroids wrap around the screen edges instead of disappearing
- Asteroid-asteroid collision with a bounce (speed-capped so they don't accelerate forever)
- Scrolling starfield background
- ESC pause menu (resume / restart / exit) with the game scene visible behind it
- Capped asteroid count so the field stays manageable

## Setup

Requires Python 3.10+ and pygame.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

> Note: make sure the virtual environment is activated, otherwise you'll get
> `ModuleNotFoundError: No module named 'pygame'`.

## Controls

| Key | Action |
| --- | --- |
| `W` | Thrust forward |
| `S` | Reverse thrust |
| `A` / `D` | Rotate left / right (inverted while reversing) |
| `Space` | Fire |
| `ESC` | Pause menu (resume / restart / exit) |

## Roadmap

- Acceleration for player movement
- Different weapon types
- Shield power-up
- Speed power-up
- Bombs that can be dropped
