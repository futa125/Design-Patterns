from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Parrot:
    _name: str

    def name(self: Parrot) -> str:
        return self._name

    def greeting(self: Parrot) -> str:
        return "Squawk"

    def menu(self: Parrot) -> str:
        return "Seeds"


def create(name: str) -> Parrot:
    return Parrot(name)
