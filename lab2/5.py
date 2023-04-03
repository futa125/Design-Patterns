from __future__ import annotations

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from statistics import median
from typing import List, Any, Union


@dataclass
class Observer(ABC):
    subject: Subject

    def __post_init__(self):
        self.subject.attach(self)

    @abstractmethod
    def update(self) -> None:
        pass


class NumberSourceStatus(Enum):
    SOURCE_EXHAUSTED = auto()


class NumberSource(ABC):
    @abstractmethod
    def generate_number(self) -> Union[int, NumberSourceStatus]:
        pass


class Subject(ABC):
    @abstractmethod
    def get_state(self) -> List:
        pass

    @abstractmethod
    def update_state(self, state: Any) -> None:
        pass

    @abstractmethod
    def attach(self, observer: Observer):
        pass

    @abstractmethod
    def detach(self, observer: Observer):
        pass

    @abstractmethod
    def notify(self):
        pass


@dataclass
class FileLogger(Observer):
    _file_path: str

    def __post_init__(self):
        self.subject.attach(self)

        with open(self._file_path, "a") as file:
            file.write(f"Logging started at {datetime.now()}\n")

    def update(self) -> None:
        with open(self._file_path, "a") as file:
            file.write(f"{datetime.now()}: {', '.join(map(str, self.subject.get_state()))}\n")


@dataclass
class SumPrinter(Observer):
    def update(self) -> None:
        print(f"Sum: {sum(self.subject.get_state())}")


@dataclass
class AveragePrinter(Observer):
    def update(self) -> None:
        print(f"Average: {sum(self.subject.get_state()) / len(self.subject.get_state()):.2f}")


@dataclass
class MedianPrinter(Observer):
    def update(self) -> None:
        print(f"Median: {median(self.subject.get_state()):.2f}")


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
    _file_path: str
    _numbers: List[int] = field(init=False, default_factory=list)

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

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update()

    def get_state(self) -> List[int]:
        return self._numbers

    def update_state(self, value: int) -> None:
        self._numbers.append(value)
        self.notify()

    def start_generating(self):
        while True:
            n = self._number_source.generate_number()
            print(f"Generated number: {n}")

            if n == NumberSourceStatus.SOURCE_EXHAUSTED:
                break

            self.update_state(n)

            time.sleep(1)


def main() -> None:
    seq = NumberSequence(KeyboardSource())
    FileLogger(seq, "output.log")
    SumPrinter(seq)
    AveragePrinter(seq)
    MedianPrinter(seq)
    seq.start_generating()

    seq = NumberSequence(FileSource("input.txt"))
    FileLogger(seq, "output.log")
    SumPrinter(seq)
    AveragePrinter(seq)
    MedianPrinter(seq)
    seq.start_generating()


if __name__ == "__main__":
    main()
