# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Asteroid properties
ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE = 0.8  # seconds
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS
ASTEROID_MIN_VERTICES = 8
ASTEROID_MAX_VERTICES = 12
ASTEROID_SPIN_MIN = -30  # degrees per second
ASTEROID_SPIN_MAX = 30  # degrees per second

# Player properties
PLAYER_RADIUS = 20
PLAYER_TURN_SPEED = 300  # degrees per second
PLAYER_SPEED = 200  # pixels per second
PLAYER_SHOOT_COOLDOWN = 0.3  # seconds
PLAYER_INVINCIBILITY_TIME = 3.0  # seconds after respawn

# Shot properties
SHOT_RADIUS = 5
PLAYER_SHOT_SPEED = 500  # pixels per second

# Collision properties
ASTEROID_BOUNCE_FACTOR = 0.5  # How much velocity changes on asteroid collision (0 = no bounce, 1 = full elastic)

# Background properties
BG_NUM_STARS = 150

# Score values
SCORE_LARGE = 20   
SCORE_MEDIUM = 50  
SCORE_SMALL = 100