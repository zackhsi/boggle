import os

# 3 minutes http://www.fun-with-words.com/play_boggle.html.
DEFAULT_GAME_DURATION_MS = 180000

# Wildcard.
WILDCARD = '*'

# Board size.
BOARD_SIZE = 16

# Environment.
DEVELOPMENT = 'development'
TESTING = 'testing'
PRODUCTION = 'production'
ENVIRONMENT = os.getenv('ENVIRONMENT', DEVELOPMENT)
VALID_ENVIRONMENTS = [DEVELOPMENT, TESTING, PRODUCTION]
if ENVIRONMENT not in VALID_ENVIRONMENTS:
    raise Exception(f'Environment "{ENVIRONMENT}" not in {VALID_ENVIRONMENTS}')

# Database.
DB_DIALECT = 'postgresql'
DB_DRIVER = 'psycopg2'
DB_USER = 'postgres'
DB_PASSWORD = ''
DB_HOST = 'localhost'
DB_PORT = '5432'
POSTGRES_URI = (
    f'{DB_DIALECT}+{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}'
)
DB_NAME = f'boggle_{ENVIRONMENT}'
DB_URI = f'{POSTGRES_URI}/{DB_NAME}'
