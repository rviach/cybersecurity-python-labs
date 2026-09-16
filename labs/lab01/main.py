"""Головний файл лабораторної роботи №1: демонстрація завдань 1-3."""

import os
import subprocess
import sys

LAB_DIR = os.path.dirname(__file__)
TASK_FILES = ["task1.py", "task2.py", "task3.py"]

for index, task_file in enumerate(TASK_FILES):
    task_path = os.path.join(LAB_DIR, task_file)
    subprocess.run([sys.executable, task_path], check=True)
    if index < len(TASK_FILES) - 1:
        print("\n" + "=" * 60 + "\n")
