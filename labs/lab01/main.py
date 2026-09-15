"""Головний файл лабораторної роботи №1: демонстрація завдань 1-3."""

import os
import sys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
)

from labs.lab01 import task1, task2, task3  # noqa: E402


def main():
    """Послідовно запускає демонстрацію всіх трьох завдань лабораторної."""
    task1.main()
    print("\n" + "=" * 60 + "\n")
    task2.main()
    print("\n" + "=" * 60 + "\n")
    task3.main()


if __name__ == "__main__":
    main()
