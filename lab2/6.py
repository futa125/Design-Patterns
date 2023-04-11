from __future__ import annotations

import ast
import logging
import re
import string
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, Set, Dict


class Subject(ABC):
    @abstractmethod
    def attach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def notify(self) -> None:
        pass


class Observer(ABC):
    @abstractmethod
    def update(self) -> None:
        pass


@dataclass
class InvalidAddress(Exception):
    _value: str

    def __str__(self) -> str:
        return f"Invalid cell address {self._value}"


@dataclass
class Address:
    _row: str
    _column: int

    def __init__(self, value: str) -> None:
        if not re.match("^([A-Z])([1-9]\\d*)$", value):
            raise InvalidAddress(value)

        self._row, self._column = re.search("^([A-Z])([1-9]\\d*)$", value).groups()

        if not re.match("^[A-Z]$", self._row):
            raise InvalidAddress(value)

        if not re.match("^[1-9]\\d*$", str(self._column)):
            raise InvalidAddress(value)

    def __hash__(self) -> int:
        return hash((self._row, self._column))

    def __repr__(self) -> str:
        return f"{self._row}{self._column}"


@dataclass
class Expression:
    value: str
    referenced_addresses: Set[Address] = field(default_factory=set, init=False)

    def __post_init__(self) -> None:
        for reference in re.findall("[A-Z][1-9]\\d*", self.value):
            self.referenced_addresses.add(Address(reference))

    def __repr__(self) -> str:
        return self.value


@dataclass
class Cell(Subject, Observer):
    _sheet: Sheet
    _address: Address
    _observers: Set[Observer] = field(default_factory=set, init=False)

    value: int = field(init=False)
    expression: Expression

    def __post_init__(self) -> None:
        self._evaluate()

    def set(self, expression: Expression) -> None:
        self.expression = expression
        self._evaluate()

    def attach(self, observer: Observer) -> None:
        self._observers.add(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update()

    def update(self) -> None:
        self._evaluate()

    def _evaluate(self) -> None:
        self.current_value = self._sheet.evaluate(self)
        self.notify()

    def __hash__(self) -> int:
        return self._address.__hash__()

    def __repr__(self) -> str:
        if self.expression == "":
            return ""

        if self.expression.value == str(self.current_value):
            return str(self.current_value)

        return f"{self.expression}={self.current_value}"


@dataclass
class Sheet:
    _row_count: int
    _column_count: int
    _cells: Dict[Address, Optional[Cell]] = field(init=False, default_factory=dict)

    def __post_init__(self) -> None:
        for row_index in range(self._row_count):
            for column_index in range(self._column_count):
                letter, number = string.ascii_uppercase[row_index], int(column_index) + 1
                self._cells[Address(f"{letter}{number}")] = None

    def cell(self, address: Address) -> Optional[Cell, None]:
        return self._cells.get(address)

    def set(self, address: Address, expression: Expression) -> None:
        logging.debug(f"Set value of {address} to {expression}")

        self._check_for_cycles(self.cell(address), expression)

        self._update_observers(address, expression)

        self.cell(address).set(expression)

    def evaluate(self, cell: Cell) -> int:
        def _eval(node: ast.expr) -> int:
            if isinstance(node, ast.Num):
                return node.n
            elif isinstance(node, ast.Name):
                return self.cell(Address(node.id)).current_value
            elif isinstance(node, ast.BinOp):
                return _eval(node.left) + _eval(node.right)
            else:
                raise Exception(f"Unsupported type {node}")

        ast_node = ast.parse(cell.expression.value, mode="eval")

        return _eval(ast_node.body)

    def get_refs(self, address: Address) -> Set[Address]:
        if self.cell(address) is None:
            return set()

        return self.cell(address).expression.referenced_addresses

    def _check_for_cycles(self, start_cell: Cell, expression: Expression) -> None:
        referenced_cells = set([self.cell(ref) for ref in expression.referenced_addresses])
        visited_cells = set()

        while start_cell not in visited_cells and len(referenced_cells) > 0:
            current_cell = referenced_cells.pop()
            if current_cell in visited_cells:
                continue

            visited_cells.add(current_cell)
            referenced_cells.update([self.cell(address) for address in current_cell.expression.referenced_addresses])

        if start_cell in visited_cells:
            raise ValueError(f"Circular reference detected")

    def _update_observers(self, address: Address, expression: Expression):
        if self.cell(address) is None:
            self._cells[address] = Cell(self, address, expression)
            current_referenced_addresses = set()
        else:
            current_referenced_addresses = self.cell(address).expression.referenced_addresses

        old_referenced_addresses = current_referenced_addresses.difference(expression.referenced_addresses)
        new_referenced_addresses = expression.referenced_addresses.difference(current_referenced_addresses)

        for old_address in old_referenced_addresses:
            self.cell(old_address).detach(self.cell(address))
            logging.debug(f"Cell {address} is no longer observing {old_address}")

        for new_address in new_referenced_addresses:
            self.cell(new_address).attach(self.cell(address))
            logging.debug(f"Cell {address} is now observing {new_address}")

    def __repr__(self) -> str:
        output = ""
        cell_sizes = [len(str(cell)) for cell in self._cells.values() if cell]

        if len(cell_sizes) == 0:
            longest_cell = len(str(None))
        else:
            longest_cell = max(cell_sizes)

        for i, value in enumerate(self._cells.values()):
            if i != 0 and i % self._column_count == 0:
                output += "\n"

            output += f"{str(value):{longest_cell + 2}}"

        output += "\n"

        return output


def main() -> None:
    logging.basicConfig(level=logging.DEBUG, format="%(message)s")

    s = Sheet(5, 5)
    print(s)

    s.set(Address("A1"), Expression("2"))
    s.set(Address("A2"), Expression("5"))
    s.set(Address("A3"), Expression("A1+A2"))
    print(s)

    s.set(Address("A1"), Expression("4"))
    s.set(Address("A4"), Expression("A1+A3"))
    print(s)

    try:
        s.set(Address("A1"), Expression("A3"))
    except ValueError as e:
        print(f"Caught exception: {e}")

    print(s)

    s.set(Address("A4"), Expression("2"))
    print(s)

    s.set(Address("B3"), Expression("A1+A3+A4"))
    print(s)

    s.set(Address("A1"), Expression("5"))
    print(s)

    s.set(Address("C5"), Expression("B3+A3"))
    print(s)

    s.set(Address("A1"), Expression("6"))
    print(s)

    s.set(Address("B3"), Expression("A1+A4+3"))
    print(s)


if __name__ == "__main__":
    main()
