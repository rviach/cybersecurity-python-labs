"""Завдання 1: Комплексний аналізатор надійності паролів (Варіант 6)."""

import os
import random
import sys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
)

from shared.student import (  # noqa: E402
    GROUP_NAME,
    STUDENT_NAME,
    VARIANT_NUMBER,
)

passwords = [
    "InfoS3c@2023",
    "simple123",
    "Def3ns3@Key",
    "public",
    "Encrypt3d#Pass",
    "basic123",
    "Secur3@Analysis",
    "temp123",
    "Pr0t3ct@Data",
    "default",
]

criteria = {
    "min_length": 8,
    "require_digits": True,
    "require_upper": True,
    "require_special": True,
}

forbidden_passwords = {
    "simple123",
    "public",
    "basic123",
    "temp123",
    "default",
    "guest",
}


def simulate_password_reuse(password_list):
    """Додає в кінець списку 3 дублікати випадково обраних паролів."""
    extended = list(password_list)
    reused_indexes = random.sample(range(len(password_list)), 3)
    for index in reused_indexes:
        extended.append(password_list[index])
    return extended


def analyze_char_classes(password):
    """Повертає словник з ознаками наявності класів символів у паролі."""
    return {
        "has_digit": any(char.isdigit() for char in password),
        "has_upper": any(char.isupper() for char in password),
        "has_lower": any(char.islower() for char in password),
        "has_special": any(not char.isalnum() for char in password),
    }


def classify_password(password, password_criteria, forbidden, occurrences):
    """Класифікує пароль за рівнем надійності відповідно до алгоритму."""
    min_length = password_criteria["min_length"]

    if password in forbidden or len(password) < min_length:
        return "Заборонений"

    classes = analyze_char_classes(password)
    required_checks = []
    if password_criteria.get("require_digits"):
        required_checks.append(classes["has_digit"])
    if password_criteria.get("require_upper"):
        required_checks.append(classes["has_upper"])
    if password_criteria.get("require_special"):
        required_checks.append(classes["has_special"])

    required_met = sum(required_checks)
    required_total = len(required_checks)

    if required_total and required_met == required_total:
        is_unique = occurrences[password] == 1
        if len(password) >= min_length + 4 and is_unique:
            return "Дуже сильний"
        return "Сильний"

    if required_met >= 1:
        return "Середній"

    return "Слабкий"


def analyze_passwords(password_list, password_criteria, forbidden):
    """Аналізує список паролів та повертає список рядків результату."""
    occurrences = {}
    for password in password_list:
        occurrences[password] = occurrences.get(password, 0) + 1

    results = []
    for index, password in enumerate(password_list, start=1):
        classes = analyze_char_classes(password)
        category = classify_password(
            password, password_criteria, forbidden, occurrences
        )
        results.append(
            {
                "index": index,
                "password": password,
                "length": len(password),
                "has_digit": classes["has_digit"],
                "has_upper": classes["has_upper"],
                "has_special": classes["has_special"],
                "category": category,
            }
        )
    return results


def print_report(results):
    """Виводить результати аналізу паролів у табличному форматі."""
    header = (
        f"{'#':<3}{'Пароль':<20}{'Довж.':<7}{'Цифра':<7}"
        f"{'Великі':<8}{'Спец.':<7}{'Категорія':<15}"
    )
    print(header)
    print("-" * len(header))
    for item in results:
        print(
            f"{item['index']:<3}{item['password']:<20}{item['length']:<7}"
            f"{str(item['has_digit']):<7}{str(item['has_upper']):<8}"
            f"{str(item['has_special']):<7}{item['category']:<15}"
        )


print(f"Студент: {STUDENT_NAME} ({GROUP_NAME}), варіант {VARIANT_NUMBER}")
print("\nЗавдання 1: Аналізатор надійності паролів\n")

extended_passwords = simulate_password_reuse(passwords)
results = analyze_passwords(extended_passwords, criteria, forbidden_passwords)
print_report(results)
