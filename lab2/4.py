import math
import random
from abc import ABC, abstractmethod
from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import List

import numpy as np


class DistributionGenerator(ABC):
    @abstractmethod
    def generate_numbers(self) -> Iterator[float]:
        pass


class PercentileCalculator(ABC):
    @abstractmethod
    def calculate_percentile(self, numbers: List[float], n: float) -> float:
        pass


@dataclass
class SequentialDistributionGenerator(DistributionGenerator):
    start: int
    stop: int
    step: int

    def generate_numbers(self) -> Iterator[float]:
        for n in range(self.start, self.stop + 1, self.step):
            yield n


@dataclass
class NormalDistributionGenerator(DistributionGenerator):
    _mean: float
    _sigma: float
    _n: int

    def generate_numbers(self) -> Iterator[float]:
        for _ in range(self._n):
            yield random.normalvariate(self._mean, self._sigma)


@dataclass
class FibonacciDistributionGenerator(DistributionGenerator):
    _n: int

    def generate_numbers(self) -> Iterator[float]:
        if self._n <= 0:
            return

        f1, f2 = 0, 1
        if self._n == 1:
            yield f1
        else:
            yield f1
            yield f2

            for _ in range(3, self._n + 1):
                f3 = f1 + f2
                yield f3

                f1 = f2
                f2 = f3


@dataclass
class NearestRankPercentileCalculator(PercentileCalculator):
    def calculate_percentile(self, numbers: List[float], percentile: float) -> float:
        numbers.sort()
        return numbers[math.ceil(percentile/100 * len(numbers)) - 1]


@dataclass
class LinearInterpolationPercentileCalculator(PercentileCalculator):
    def calculate_percentile(self, numbers: List[float], percentile: float) -> float:
        numbers.sort()
        return np.percentile(numbers, percentile)  # Second variant (C=1)


@dataclass
class DistributionTester:
    numbers: List[float] = field(init=False, default_factory=list)
    _distributions_generator: DistributionGenerator
    _percentile_calculator: PercentileCalculator

    def __post_init__(self):
        for n in self._distributions_generator.generate_numbers():
            self.numbers.append(round(n, 2))

    def calculate_percentiles(self, percentiles: List[int]) -> List[float]:
        results = []
        for n in percentiles:
            results.append(
                round(self._percentile_calculator.calculate_percentile(self.numbers, n), 2))

        return results


def main():
    generators = [
        SequentialDistributionGenerator(5, 50, 5),
        NormalDistributionGenerator(25, 5, 10),
        FibonacciDistributionGenerator(10),
    ]

    calculators = [
        NearestRankPercentileCalculator(),
        LinearInterpolationPercentileCalculator(),
    ]

    percentiles = [n for n in range(10, 100, 10)]

    for generator in generators:
        for calculator in calculators:
            tester = DistributionTester(generator, calculator)
            results = tester.calculate_percentiles(percentiles)

            print(f"{generator.__class__.__name__} + {calculator.__class__.__name__}")
            print(f"Generated numbers: {tester.numbers}")
            print(f"Percentiles: {percentiles}")
            print(f"Result: {results}")
            print()


if __name__ == "__main__":
    main()
