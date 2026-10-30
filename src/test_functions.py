import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

from app_functions import (
    calc_discount,
    pluralize_items,
    format_full_name,
    get_client_tier,
    get_client_loyalty_days,
)


def test_calc_discount():
    assert calc_discount(None, 10) == 0.0
    assert calc_discount(1000, None) == 0.0
    assert calc_discount("abc", 10) == 0.0
    assert calc_discount(1000, -5) == 1000.0
    assert calc_discount(1000, 0) == 1000.0
    assert calc_discount(1000, 20) == 800.0
    assert calc_discount(1000, 100) == 0.0
    assert calc_discount(999.99, 10) == 899.99
    print("test_calc_discount OK")


def test_pluralize_items():
    assert pluralize_items(1) == "1 товар"
    assert pluralize_items(2) == "2 товара"
    assert pluralize_items(5) == "5 товаров"
    assert pluralize_items(11) == "11 товаров"
    assert pluralize_items(21) == "21 товар"
    assert pluralize_items(22) == "22 товара"
    assert pluralize_items(0) == "0 товаров"
    assert pluralize_items(None) == "0 товаров"
    assert pluralize_items("abc") == "0 товаров"
    print("test_pluralize_items OK")


def test_format_full_name():
    assert format_full_name(None, "Иван", "Иванович") == "Аноним"
    assert format_full_name("", "Иван", "Иванович") == "Аноним"
    assert format_full_name("Иванов", None, "Иванович") == "Аноним"
    assert format_full_name("  иванов ", " иван ", " иванович ") == "Иванов И.И."
    assert format_full_name("Иванов", "Иван", None) == "Иванов И."
    assert format_full_name("Иванов", "Иван", "") == "Иванов И."
    print("test_format_full_name OK")


def test_get_client_tier():
    assert get_client_tier(None) == "Без статуса"
    assert get_client_tier(-1) == "Без статуса"
    assert get_client_tier(0) == "Новичок"
    assert get_client_tier(4999) == "Новичок"
    assert get_client_tier(5000) == "Бронза"
    assert get_client_tier(19999) == "Бронза"
    assert get_client_tier(20000) == "Серебро"
    assert get_client_tier(50000) == "Золото"
    assert get_client_tier(100000) == "Платина"
    print("test_get_client_tier OK")


def test_get_client_loyalty_days():
    assert get_client_loyalty_days(None) == 0
    assert get_client_loyalty_days("") == 0
    assert get_client_loyalty_days("не дата") == 0
    days = get_client_loyalty_days("2024-01-01")
    assert isinstance(days, int)
    assert days >= 0
    print("test_get_client_loyalty_days OK")


if __name__ == "__main__":
    test_calc_discount()
    test_pluralize_items()
    test_format_full_name()
    test_get_client_tier()
    test_get_client_loyalty_days()
    print("ALL TESTS PASSED")