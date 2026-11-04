# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Asteroid properties
ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE = 1.2  # seconds
ASTEROID_MAX_COUNT = 12  # max simultaneous asteroids (they wrap around, so without this the field grows unboundedly)
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS
ASTEROID_MIN_VERTICES = 8
ASTEROID_MAX_VERTICES = 12
ASTEROID_SPIN_MIN = -30  # degrees per second
ASTEROID_SPIN_MAX = 30  # degrees per second

# Player properties
PLAYER_RADIUS = 20
PLAYER_TURN_SPEED = 280  # degrees per second
PLAYER_ACCELERATION = 150  # pixels per second^2 while thrusting (calm base flight)
PLAYER_MAX_SPEED = 150  # pixels per second; base top speed (calm flight)
PLAYER_DRAG = 1  # per-second velocity decay when not thrusting
PLAYER_SHOOT_COOLDOWN = 0.3  # seconds
PLAYER_INVINCIBILITY_TIME = 3.0  # seconds after respawn

# Shot properties
SHOT_RADIUS = 5
PLAYER_SHOT_SPEED = 500  # pixels per second

# Collision properties
ASTEROID_BOUNCE_FACTOR = 0.5  # How much velocity changes on asteroid collision (0 = no bounce, 1 = full elastic)
ASTEROID_MAX_SPEED = 200  # pixels per second; caps asteroid speed so repeated bounces don't accelerate them unboundedly

# Background properties
BG_NUM_STARS = 150

# Score values
SCORE_LARGE = 20   
SCORE_MEDIUM = 50  
SCORE_SMALL = 100

# Particle (explosion) properties
PARTICLE_COUNT_MIN = 15
PARTICLE_COUNT_MAX = 40
PARTICLE_SPEED_MIN = 50   # pixels per second
PARTICLE_SPEED_MAX = 200  # pixels per second
PARTICLE_SIZE_MIN = 2     # initial radius in pixels
PARTICLE_SIZE_MAX = 5     # initial radius in pixels
PARTICLE_LIFETIME_MIN = 0.4  # seconds
PARTICLE_LIFETIME_MAX = 0.8  # seconds
PARTICLE_COLOR = (255, 255, 255)

# Pickup properties
PICKUP_RADIUS = 14
PICKUP_LIFETIME = 12  # seconds before a pickup expires
PICKUP_DRIFT_SPEED = 30  # pixels per second
# Per-kind drop tuning: chance a destroyed small asteroid drops this kind,
# and the max number of that kind allowed on screen at once.
PICKUP_DROPS = {
    "weapon": {"rate": 0.15, "max_count": 2},
    "shield": {"rate": 0.10, "max_count": 2},
    "life":   {"rate": 0.05, "max_count": 1},
    "speed":  {"rate": 0.08, "max_count": 2},
}

# Shield power-up
SHIELD_DURATION = 8.0  # seconds of invincibility granted
SHIELD_COLOR = (80, 180, 255)

# Life restore power-up
PLAYER_MAX_LIVES = 3
LIFE_PICKUP_COLOR = (255, 80, 80)

# Speed power-up
SPEED_DURATION = 8.0  # seconds of boosted speed granted
SPEED_MULTIPLIER = 2.0  # multiplier applied to the player's max speed (boosted = 340 px/s, the old baseline)
SPEED_COLOR = (255, 220, 80)

# Bomb properties
BOMB_COUNT = 3  # bombs available per life
BOMB_RADIUS = 8
BOMB_SPEED = 150  # pixels per second, drifts behind the ship
BOMB_EXPLOSION_RADIUS = 120  # asteroids within this distance are destroyed
BOMB_COLOR = (255, 100, 100)