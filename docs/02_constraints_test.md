 Результаты проверки ограничений

| Ограничение | Ожидаемый результат | Фактический результат | Статус |
|-------------|---------------------|-----------------------|--------|
| UNIQUE на login | ошибка | ошибка: UNIQUE constraint failed: users.login | пройден |
| NOT NULL на last_name | ошибка | ошибка: NOT NULL constraint failed: users.last_name | пройден |
| CHECK на price | ошибка | ошибка: CHECK constraint failed: price > 0 | пройден |
| CHECK на quantity | ошибка | ошибка: CHECK constraint failed: quantity >= 0 | пройден |
| FOREIGN KEY на role_id | ошибка | ошибка: FOREIGN KEY constraint failed | пройден |
| ON DELETE RESTRICT | ошибка | ошибка: FOREIGN KEY constraint failed | пройден |
| ON DELETE CASCADE | каскадное удаление | каскадное удаление | пройден |