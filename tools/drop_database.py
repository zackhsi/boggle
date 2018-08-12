from sqlalchemy.exc import ProgrammingError

from boggle.database import cluster_engine
from boggle.settings import DB_NAME


def main() -> None:
    print(f'Drop database {DB_NAME}? ["yes" to confirm]')
    while True:
        choice = input().lower()
        if choice == 'yes':
            break
        print('Respond "yes" to proceed.')

    connection = cluster_engine.connect()
    connection.execute('commit')
    try:
        connection.execute(f'drop database {DB_NAME}')
    except ProgrammingError as e:
        if 'does not exist' not in str(e):
            raise
        print(f'Database {DB_NAME} does not exist')
    else:
        print(f'Dropped database {DB_NAME}')
    connection.close()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
