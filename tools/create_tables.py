import time

from sqlalchemy.exc import ProgrammingError

from boggle import models
from boggle.database import Base, cluster_engine
from boggle.settings import DB_NAME


def main() -> None:
    for attempt in range(5):
        try:
            connection = cluster_engine.connect()
        except Exception:
            print('Failed to connect to database, sleeping 1s...')
            time.sleep(1)
    connection.execute('commit')
    try:
        connection.execute(f'create database {DB_NAME}')
    except ProgrammingError as e:
        if 'already exists' not in str(e):
            raise
    else:
        print(f'Created database {DB_NAME}')
    connection.close()

    models.load()
    Base.metadata.create_all()

    print('Tables:')
    for table_name in Base.metadata.tables.keys():
        print(f'    - {table_name}')


if __name__ == '__main__':
    main()
