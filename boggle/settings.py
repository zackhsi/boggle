# 3 minutes http://www.fun-with-words.com/play_boggle.html.
DEFAULT_GAME_DURATION_MS = 180000

# Database settings.
DB_DIALECT = 'postgresql'
DB_DRIVER = 'psycopg2'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = ''
DB_CONNECTION_STRING = (
    f'{DB_DIALECT}+{DB_DRIVER}://'
    f'{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
)
