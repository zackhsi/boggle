import os

# 3 minutes http://www.fun-with-words.com/play_boggle.html.
DEFAULT_GAME_DURATION_MS = 180000

# Wildcard.
WILDCARD = '*'

# Board size.
BOARD_SIZE = 16

# Word not found reason.
REASON_NOT_IN_DICTIONARY_FMT = '{word} is not in the dictionary!'
REASON_NOT_IN_BOARD_FMT = '{word} is not in the board!'

# Environment.
DEVELOPMENT = 'development'
TESTING = 'testing'
PRODUCTION = 'production'
ENVIRONMENT = os.getenv('ENVIRONMENT') or DEVELOPMENT
VALID_ENVIRONMENTS = [DEVELOPMENT, TESTING, PRODUCTION]
if ENVIRONMENT not in VALID_ENVIRONMENTS:
    raise Exception(f'Environment "{ENVIRONMENT}" not in {VALID_ENVIRONMENTS}')

# Dictionary.
if ENVIRONMENT == TESTING:
    # Speed up test runs.
    DICTIONARY_PATH = 'data/dictionary_test.txt'
else:
    DICTIONARY_PATH = 'data/dictionary.txt'
DICTIONARY_VARIANT = 'marisa_trie'

# Database.
DB_DIALECT = 'postgresql'
DB_DRIVER = 'psycopg2'
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_HOST = os.getenv('POSTGRES_PORT_5432_TCP_ADDR', 'localhost')
DB_PORT = '5432'
POSTGRES_URI = (
    f'{DB_DIALECT}+{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}'
)
DB_NAME = f'boggle_{ENVIRONMENT}'
DB_URI = f'{POSTGRES_URI}/{DB_NAME}'
