from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Tiger:
    _name: str

    def name(self: Tiger) -> str:
        return self._name

    def greeting(self: Tiger) -> str:
        return "Rawr"

    def menu(sel: Tiger) -> str:
        return "Antelopes"


def create(name: str) -> Tiger:
    return Tiger(name)
