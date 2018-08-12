from importlib import import_module
from pkgutil import walk_packages


def load() -> None:
    modules = walk_packages(__path__, prefix=f'{__name__}.')  # type: ignore
    for _, module_name, _ in modules:
        import_module(module_name)
