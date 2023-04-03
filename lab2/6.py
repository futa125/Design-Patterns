from __future__ import annotations

import ast
import re
import string
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Set


class Subject(ABC):
    @abstractmethod
    def attach(self, observer: Observer):
        pass

    @abstractmethod
    def detach(self, observer: Observer):
        pass

    @abstractmethod
    def detach_all(self):
        pass

    @abstractmethod
    def notify(self):
        pass


class Observer(ABC):
    @abstractmethod
    def update(self):
        pass


@dataclass(eq=False)  # Makes the class hashable
class Cell(Subject, Observer):
    _sheet: Sheet
    expression: str
    value: int = field(init=False)
    observers: Set[Observer] = field(default_factory=set, init=False)

    def __post_init__(self):
        self.evaluate()

    def set_expression(self, expression: str) -> None:
        self.expression = expression
        self.evaluate()

    def evaluate(self) -> None:
        self.value = self._sheet.evaluate(self)
        self.notify()

    def attach(self, observer: Observer):
        self.observers.add(observer)

    def detach(self, observer: Observer):
        self.observers.remove(observer)

    def detach_all(self):
        self.observers.clear()

    def notify(self):
        for observer in self.observers:
            observer.update()

    def update(self):
        self.evaluate()

    def __repr__(self) -> str:
        if self.expression == "":
            return ""

        if self.expression == str(self.value):
            return str(self.value)

        return f"{self.expression}={self.value}"


@dataclass
class Sheet:
    _row_count: int
    _column_count: int
    _cells: List[List[Optional[Cell]]] = field(init=False, default_factory=list)

    def __post_init__(self):
        for _ in range(self._row_count):
            self._cells.append([None for _ in range(self._column_count)])

        self.print()

    def cell(self, ref: str):
        i, j = self._ref_to_index(ref)

        return self._cells[i][j]

    def set(self, ref: str, expression: str):
        if self.cell(ref) is None:
            i, j = self._ref_to_index(ref)
            self._cells[i][j] = Cell(self, expression)

        self._check_for_cycles(ref, expression)

        new_refs = set(self.get_refs_from_expression(expression))
        old_refs = set(self.get_refs(self.cell(ref))).difference(new_refs)

        for old_ref in old_refs:
            self.cell(old_ref).detach(self.cell(ref))
            print(f"Cell {ref} is no longer observing {old_ref}")

        for new_ref in new_refs:
            self.cell(new_ref).attach(self.cell(ref))
            print(f"Cell {ref} is now observing {new_ref}")

        self.cell(ref).set_expression(expression)

    def _check_for_cycles(self, ref: str, expression: str):
        cell = self.cell(ref)

        cells_queue = set([self.cell(ref) for ref in self.get_refs_from_expression(expression)])
        cells_visited = set()

        while cell not in cells_visited and cells_queue:
            current_cell = cells_queue.pop()
            if current_cell in cells_visited:
                continue

            cells_visited.add(current_cell)

            children = [self.cell(ref) for ref in self.get_refs(current_cell)]
            cells_queue.update([cell for cell in children if cell not in cells_visited])

        if cell in cells_visited:
            raise RuntimeError("Circular reference detected!")

    def get_refs(self, cell: Cell) -> List[str]:
        return self.get_refs_from_expression(cell.expression)

    @staticmethod
    def get_refs_from_expression(expression: str) -> List[str]:
        return re.findall("[A-Z][0-9]+", expression)

    def evaluate(self, cell: Cell):
        return self.eval_expression(cell.expression)

    def eval_expression(self, exp) -> int:
        def _eval(node: ast.expr) -> complex | int:
            if isinstance(node, ast.Num):
                return node.n
            elif isinstance(node, ast.Name):
                return self.cell(node.id).value
            elif isinstance(node, ast.BinOp):
                return _eval(node.left) + _eval(node.right)
            else:
                raise Exception(f"Unsupported type {node}")

        ast_node = ast.parse(exp, mode="eval")

        return _eval(ast_node.body)

    def print(self):
        for row in self._cells:
            for item in row:
                print(f"{str(item):10}", end="\t")

            print()

    @staticmethod
    def _ref_to_index(ref: str) -> (int, int):
        groups = re.search(r"([A-Z])(\d+)", ref).groups()
        letter, number = groups

        return string.ascii_uppercase.index(letter), int(number) - 1


def main() -> None:
    s = Sheet(5, 5)
    print()

    s.set("A1", "2")
    s.set("A2", "5")
    s.set("A3", "A1+A2")
    s.print()
    print()

    s.set("A1", "4")
    s.set("A4", "A1+A3")
    s.print()
    print()

    try:
        s.set("A1", "A3")
    except RuntimeError as e:
        print(f"Caught exception: {e}")

    s.print()
    print()

    s.set("A4", "2")
    s.print()
    print()

    s.set("B3", "A1+A3+A4")
    s.print()
    print()

    s.set("A1", "5")
    s.print()
    print()

    s.set("C5", "B3+A3")
    s.print()
    print()

    s.set("A1", "6")
    s.print()
    print()


if __name__ == "__main__":
    main()
