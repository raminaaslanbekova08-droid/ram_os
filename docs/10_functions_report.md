 Day 10. Functions and procedures report

 1. Созданные функции

- calc_discount(price, discount_percent) — расчёт цены со скидкой.
- pluralize_items(count) — склонение слова «товар».
- format_full_name(last, first, middle) — форматирование ФИО.
- get_client_tier(total_spent) — определение уровня клиента.
- get_client_loyalty_days(first_order_date) — количество дней с первого заказа.
- place_order(...) — эмуляция процедуры создания заказа.
- cancel_order(...) — эмуляция процедуры отмены заказа.

 2. Результаты SQL-запросов

Вставить сюда вывод 5 запросов из queries/10_advanced_queries.sql.

 3. Транзакции

В place_order и cancel_order используется try/except:
- при ошибке вызывается conn.rollback();
- при успехе conn.commit().

 4. Unit-тесты

Команда:
python src/test_functions.py

Результат:
ALL TESTS PASSED