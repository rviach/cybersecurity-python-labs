"""Завдання 2: Багаторівнева система контролю доступу (Варіант 6)."""

import os
import sys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
)

from shared.student import (  # noqa: E402
    GROUP_NAME,
    STUDENT_NAME,
    VARIANT_NUMBER,
)

users = {
    "red_team_lead": {
        "role": "red_team",
        "clearance": 4,
        "department": "Red Team",
        "active": True,
    },
    "blue_team_analyst": {
        "role": "blue_team",
        "clearance": 3,
        "department": "Blue Team",
        "active": True,
    },
    "purple_team_coord": {
        "role": "purple_team",
        "clearance": 3,
        "department": "Purple Team",
        "active": True,
    },
    "student_intern": {
        "role": "student",
        "clearance": 1,
        "department": "Academia",
        "active": True,
    },
    "retired_expert": {
        "role": "retired",
        "clearance": 2,
        "department": "Emeritus",
        "active": False,
    },
}

resources = [
    ("attack_scenarios", 4),
    ("defense_playbooks", 3),
    ("exercise_plans", 3),
    ("research_papers", 1),
    ("exploit_tools", 4),
    ("student_resources", 1),
    ("simulation_results", 3),
    ("red_team_tools", 4),
    ("blue_team_reports", 3),
    ("public_research", 1),
]

security_levels = ("Academic", "Operational", "Tactical", "Strategic")

blocked_users = {"retired_expert", "academic_violator", "leaked_account"}


def print_resources(resource_list, level_names):
    """Виводить список ресурсів із текстовою назвою рівня безпеки."""
    print("Ресурси системи:")
    for name, level in resource_list:
        print(f"  {name:<25} -> {level_names[level - 1]}")


def check_access(
    username, resource_name, resource_level, user_directory, blocked
):
    """Перевіряє доступ користувача до ресурсу за алгоритмом варіанту."""
    if username not in user_directory:
        return False, "User not found"

    if username in blocked:
        return False, "User is blocked"

    account = user_directory[username]
    if not account["active"]:
        return False, "Account inactive"

    if account["clearance"] >= resource_level:
        return True, ""

    return False, "Insufficient clearance"


def run_access_checks(user_directory, resource_list, blocked):
    """Перевіряє доступ кожного користувача до кожного ресурсу."""
    lines = []
    for username in user_directory:
        for resource_name, resource_level in resource_list:
            allowed, reason = check_access(
                username,
                resource_name,
                resource_level,
                user_directory,
                blocked,
            )
            if allowed:
                lines.append(
                    f"user={username} resource={resource_name} -> ALLOW"
                )
            else:
                lines.append(
                    f"user={username} resource={resource_name} "
                    f"-> DENY ({reason})"
                )
    return lines


def main():
    """Точка входу для демонстрації системи контролю доступу."""
    print(f"Студент: {STUDENT_NAME} ({GROUP_NAME}), варіант {VARIANT_NUMBER}")
    print("\nЗавдання 2: Система контролю доступу\n")

    print_resources(resources, security_levels)

    print("\nРезультати перевірки доступу:")
    for line in run_access_checks(users, resources, blocked_users):
        print(f"  {line}")


if __name__ == "__main__":
    main()
