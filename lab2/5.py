from __future__ import annotations

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from statistics import median
from typing import List, Union


class NumberSourceStatus(Enum):
    SOURCE_EXHAUSTED = auto()


class NumberSource(ABC):
    @abstractmethod
    def generate_number(self) -> Union[int, NumberSourceStatus]:
        pass


@dataclass
class Observer(ABC):
    @abstractmethod
    def update(self, state: List[int]) -> None:
        pass


class Subject(ABC):
    @abstractmethod
    def attach(self, *observers: Observer) -> None:
        pass

    @abstractmethod
    def detach(self, *observers: Observer) -> None:
        pass

    @abstractmethod
    def notify(self) -> None:
        pass


@dataclass
class FileLogger(Observer):
    _file_path: str

    def __post_init__(self) -> None:
        with open(self._file_path, "a") as file:
            file.write(f"Logging started at {datetime.now()}\n")

    def update(self, state: List[int]) -> None:
        with open(self._file_path, "a") as file:
            file.write(f"{datetime.now()}: {', '.join(map(str, state))}\n")


@dataclass
class SumPrinter(Observer):
    def update(self, state: List[int]) -> None:
        print(f"Sum: {sum(state)}")


@dataclass
class AveragePrinter(Observer):
    def update(self, state: List[int]) -> None:
        print(f"Average: {sum(state) / len(state):.2f}")


@dataclass
class MedianPrinter(Observer):
    def update(self, state: List[int]) -> None:
        print(f"Median: {median(state):.2f}")


@dataclass
class KeyboardSource(NumberSource):
    def generate_number(self) -> Union[int, NumberSourceStatus]:
        while True:
            value = input("Enter a number: ")

            if value == "q" or value == "quit" or value == "exit":
                return NumberSourceStatus.SOURCE_EXHAUSTED

            try:
                value = int(value)
            except ValueError:
                print("Invalid input!")
                continue

            return value


@dataclass
class FileSource(NumberSource):
    _numbers: List[int] = field(init=False, default_factory=list)
    _file_path: str

    def __post_init__(self) -> None:
        with open(self._file_path, "r") as file:
            for line in file.readlines():
                values = line.split(",")
                for value in values:
                    value = value.strip()

                    try:
                        value = int(value)
                    except ValueError:
                        print("Invalid input!")
                        continue

                    self._numbers.append(value)

    def generate_number(self) -> Union[int, NumberSourceStatus]:
        if len(self._numbers) == 0:
            return NumberSourceStatus.SOURCE_EXHAUSTED

        return self._numbers.pop(0)  # Left pop


@dataclass
class NumberSequence(Subject):
    _observers: List[Observer] = field(default_factory=list, init=False)
    _numbers: List[int] = field(default_factory=list, init=False)
    _number_source: NumberSource

    def attach(self, *observers: Observer) -> None:
        for observer in observers:
            self._observers.append(observer)

    def detach(self, *observers: Observer) -> None:
        for observer in observers:
            self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self._numbers)

    def start_generating(self) -> None:
        while True:
            n = self._number_source.generate_number()
            print(f"Generated number: {n}")

            if n == NumberSourceStatus.SOURCE_EXHAUSTED:
                break

            self._numbers.append(n)
            self.notify()

            time.sleep(1)


def main() -> None:
    seq = NumberSequence(KeyboardSource())
    file_logger = FileLogger("output.log")
    sum_printer = SumPrinter()
    average_printer = AveragePrinter()
    median_printer = MedianPrinter()
    seq.attach(file_logger, sum_printer, average_printer, median_printer)
    seq.start_generating()

    seq = NumberSequence(FileSource("input.txt"))
    seq.attach(file_logger, sum_printer, average_printer, median_printer)
    seq.start_generating()


if __name__ == "__main__":
    main()
