import subprocess

from sqlalchemy.exc import ProgrammingError

from boggle import models
from boggle.database import Base, cluster_engine
from boggle.settings import DB_NAME


def main() -> None:
    try:
        subprocess.check_output(
            [
                'createuser',
                '--superuser',
                'postgres',
            ],
            stderr=subprocess.STDOUT
        )
    except subprocess.CalledProcessError as e:
        if 'already exists' not in e.stdout.decode():
            raise
    else:
        print(f'Created postgres user')

    connection = cluster_engine.connect()
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
