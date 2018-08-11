import subprocess
from importlib import import_module
from pkgutil import walk_packages

from boggle import models
from boggle.database import Base


def main() -> None:
    print('Creating postgres user...')
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

    print('Creating tables...')
    modules = walk_packages(models.__path__, prefix=f'{models.__name__}.')
    for _, module_name, _ in modules:
        import_module(module_name)
    Base.metadata.create_all()

    print('Tables:')
    for table_name in Base.metadata.tables.keys():
        print(f'    - {table_name}')


if __name__ == '__main__':
    main()
