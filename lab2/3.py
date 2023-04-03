from typing import Any, Callable, Iterable


def my_max(iterable: Iterable[Any], key: Callable[[Any], Any] = lambda x: x) -> Any:
    max_value: Any = None

    for x in iterable:
        if max_value is None or key(x) > key(max_value):
            max_value = x

    return max_value


def main() -> None:
    ints = [1, 3, 5, 7, 4, 6, 9, 2, 0]
    string = "Suncana strana ulice"
    strings = ["Gle", "malu", "vocku", "poslije", "kise",
               "Puna", "je", "kapi", "pa", "ih", "njise"]
    prices = {"burek": 8, "buhtla": 5}
    names = [("José", "Mourinho"), ("Giovanni", "Giorgio"),
             ("Thomasina", "Ashlea"), ("Anita", "Emma"), ("Juan", "Mourinho")]

    print(my_max(ints))
    print(my_max(ints, lambda x: -x))
    print(my_max(string))
    print(my_max(string, lambda x: -ord(x)))
    print(my_max(strings))
    print(my_max(strings, len))
    print(my_max(prices, prices.get))
    print(my_max(names, lambda x: (x[1], x[0])))


if __name__ == "__main__":
    main()
