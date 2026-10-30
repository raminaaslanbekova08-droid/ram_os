 Отчёт по Дню 10. Хранимые процедуры и функции

 1. Чем отличается функция от процедуры

Функция — это блок кода, который обязательно возвращает значение: число, строку или таблицу. Функцию удобно вызывать внутри `SELECT`, например `SELECT calculate_total(1000, 3)`. Функция обычно не должна менять данные.

Процедура — это блок кода, который выполняет действия и может изменять данные: `INSERT`, `UPDATE`, `DELETE`. Процедура не обязана возвращать значение. В PostgreSQL она вызывается через `CALL`, например `CALL create_order_pg(1, 2, 1)`. В SQLite процедур нет, поэтому в Python мы эмулируем их обычными функциями, которые управляют транзакцией.

 2. Результаты Python-функций

 Задание 1.1. `calc_order_total`

```python
def calc_order_total(price, quantity):
    if price is None or quantity is None:
        return 0
    if quantity <= 0:
        return 0
    return float(price) * int(quantity)
Регистрация:

python
conn.create_function("calculate_total", 2, calc_order_total)
Пример выполнения:


calculate_total(1000, 3) = 3000.0
calculate_total(1000, 0) = 0