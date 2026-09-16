"""Завдання 3: Безпечне хешування, CSV-база та JSON-логування (Варіант 6)."""

import csv
import functools
import hashlib
import json
import os
import sys
from datetime import datetime

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
)

from shared.student import (
    GROUP_NAME,
    STUDENT_NAME,
    VARIANT_NUMBER,
)

HASH_ALGORITHM = "blake2s"
MIN_PASSWORD_LENGTH = 9
PERSONAL_SALT = str(VARIANT_NUMBER).zfill(5)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
USERS_CSV_PATH = os.path.join(DATA_DIR, "users.csv")
LOG_JSON_PATH = os.path.join(DATA_DIR, "log.json")


class ValidationError(Exception):
    """Виникає, якщо пароль не відповідає мінімальній довжині варіанту."""


def generate_hash(password: str, salt: str = "00000") -> str:
    """Повертає шістнадцятковий хеш конкатенації пароля та солі."""
    if not password or not salt:
        raise ValueError("Пароль та сіль не можуть бути порожніми.")
    if len(password) < MIN_PASSWORD_LENGTH:
        raise ValidationError(
            f"Пароль повинен містити щонайменше "
            f"{MIN_PASSWORD_LENGTH} символів."
        )
    digest = hashlib.new(HASH_ALGORITHM, (password + salt).encode("utf-8"))
    return digest.hexdigest()


users_to_register = (
    ("agent_smith", "Matr1x@Secure"),
    ("cipher_queen", "Qu@ntumLeap99"),
    ("night_owl", "N0ct#urnalFlight"),
    ("byte_hunter", "Byt3Hunt3r2024"),
    ("root_keeper", "R00t@Keeper1"),
    ("shadow_admin", "Sh@dowAdmin77"),
    ("packet_diver", "P@cketDiver321"),
    ("vault_master", "V@ultM4ster1"),
    ("blue_falcon", "Blu3F@lcon2024"),
    ("iron_clad", "abc"),
)


def create_user(username, password):
    """Створює пару (логін, хеш) для одного користувача."""
    hash_value = generate_hash(password, PERSONAL_SALT)
    return username, hash_value


def create_users(users_list):
    """Записує список користувачів у CSV-базу, пропускаючи некоректні."""
    os.makedirs(DATA_DIR, exist_ok=True)
    created = []
    try:
        with open(
            USERS_CSV_PATH, "w", newline="", encoding="utf-8"
        ) as csv_file:
            writer = csv.writer(csv_file)
            for username, password in users_list:
                try:
                    login_name, hash_value = create_user(username, password)
                    writer.writerow([login_name, hash_value])
                    created.append((login_name, hash_value))
                except (ValueError, ValidationError) as exc:
                    print(f"  [!] Пропущено користувача '{username}': {exc}")
    except (FileNotFoundError, PermissionError, IOError) as exc:
        print(f"  [!] Помилка запису файлу бази користувачів: {exc}")
    return created


def read_users_db():
    """Читає базу користувачів із CSV-файлу у список пар (логін, хеш)."""
    users_db = []
    try:
        with open(USERS_CSV_PATH, newline="", encoding="utf-8") as csv_file:
            for row in csv.reader(csv_file):
                if row:
                    users_db.append((row[0], row[1]))
    except (FileNotFoundError, PermissionError, IOError) as exc:
        print(f"  [!] Не вдалося прочитати базу користувачів: {exc}")
    return users_db


def print_users_db(users_db):
    """Виводить базу користувачів у вигляді структурованої таблиці."""
    print(f"{'Логін':<20}{'Хеш пароля':<70}")
    print("-" * 90)
    for username, hash_value in users_db:
        print(f"{username:<20}{hash_value:<70}")


def _read_log_entries():
    """Повертає список подій із log.json або порожній список."""
    if not os.path.exists(LOG_JSON_PATH):
        return []
    try:
        with open(LOG_JSON_PATH, encoding="utf-8") as log_file:
            return json.load(log_file)
    except (FileNotFoundError, PermissionError, IOError, json.JSONDecodeError):
        return []


def _write_log_entries(entries):
    """Записує повний список подій у log.json."""
    os.makedirs(DATA_DIR, exist_ok=True)
    try:
        with open(LOG_JSON_PATH, "w", encoding="utf-8") as log_file:
            json.dump(entries, log_file, indent=4, ensure_ascii=False)
    except (FileNotFoundError, PermissionError, IOError) as exc:
        print(f"  [!] Не вдалося записати журнал подій: {exc}")


def log_event(func):
    """Логує кожну спробу входу, не зберігаючи пароль у відкритому вигляді."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        username = args[0] if args else kwargs.get("username", "")
        status = "failure"
        try:
            success = func(*args, **kwargs)
            status = "success" if success else "failure"
            return success
        finally:
            entries = _read_log_entries()
            entries.append(
                {
                    "event": "login",
                    "user": username,
                    "result": status,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "args": [username],
                    "kwargs": {},
                }
            )
            _write_log_entries(entries)

    return wrapper


@log_event
def login(username: str, password: str) -> bool:
    """Перевіряє логін/пароль користувача проти збереженого хешу."""
    if not username or not password:
        raise ValueError("Логін та пароль не можуть бути порожніми.")

    users_db = dict(read_users_db())
    if username not in users_db:
        return False

    try:
        candidate_hash = generate_hash(password, PERSONAL_SALT)
    except ValidationError:
        return False

    return users_db[username] == candidate_hash


def demonstrate_authentication():
    """Демонструє успішні, невдалі та помилкові спроби входу."""
    print("\nАвтентифікація користувачів:")
    demo_attempts = [
        (users_to_register[0][0], users_to_register[0][1]),
        (users_to_register[1][0], "WrongPassword123"),
        ("unknown_user", "SomePassword123"),
        ("", ""),
    ]
    for username, password in demo_attempts:
        try:
            success = login(username, password)
            status = "успішно" if success else "відмовлено"
            print(f"  login('{username}') -> {status}")
        except ValueError as exc:
            print(f"  login('{username}') -> помилка: {exc}")


print(f"Студент: {STUDENT_NAME} ({GROUP_NAME}), варіант {VARIANT_NUMBER}")
print(
    f"\nЗавдання 3: Хешування ({HASH_ALGORITHM}), CSV-база, JSON-логування\n"
)

print("Реєстрація користувачів...")
created = create_users(users_to_register)
print(f"  Успішно зареєстровано: {len(created)} з {len(users_to_register)}")

users_db = read_users_db()
print("\nВміст бази даних users.csv:")
print_users_db(users_db)

demonstrate_authentication()
