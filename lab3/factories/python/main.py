import os

from typing import Any, Callable, Tuple
from importlib import import_module

PLUGINS_DIR = "plugins"
PLUGIN_EXTENSION = ".py"
CREATE_FUNCTION = "create"


def factory(module_name) -> Callable[[str], Any]:
    module = import_module(f"{PLUGINS_DIR}.{module_name}")

    return getattr(module, CREATE_FUNCTION)


def print_greeting(pet: Any):
    print(f"{pet.name()} says {pet.greeting()}")


def print_menu(pet: Any):
    print(f"{pet.name()} likes to eat {pet.menu()}")


def main():
    pets = []

    for module in os.listdir(PLUGINS_DIR):
        module_name, module_extension = os.path.splitext(module)

        if module_extension == PLUGIN_EXTENSION:
            pet = factory(module_name)(f"{module_name.capitalize()}")
            pets.append(pet)

    for pet in pets:
        print_greeting(pet)
        print_menu(pet)


if __name__ == "__main__":
    main()
