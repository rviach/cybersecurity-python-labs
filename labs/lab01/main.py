"""Головний файл лабораторної роботи №1: демонстрація завдань 1-3."""

import os
import sys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
)

from labs.lab01 import task1  # noqa: E402,F401

print("\n" + "=" * 60 + "\n")

from labs.lab01 import task2  # noqa: E402,F401

print("\n" + "=" * 60 + "\n")

from labs.lab01 import task3  # noqa: E402

task3.main()
