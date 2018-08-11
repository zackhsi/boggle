from importlib import import_module
from pkgutil import walk_packages

from boggle import models
from boggle.database import Base


def main() -> None:
    print('Drop all tables?')
    modules = walk_packages(models.__path__, prefix=f'{models.__name__}.')
    for _, module_name, _ in modules:
        import_module(module_name)
    for table_name in Base.metadata.tables.keys():
        print(f'    - {table_name}')
    print('["yes" to confirm]')
    while True:
        choice = input().lower()
        if choice == 'yes':
            break
        print('Respond "yes" to proceed.')
    Base.metadata.drop_all()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
