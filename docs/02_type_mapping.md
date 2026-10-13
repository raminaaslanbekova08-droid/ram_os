 Сопоставление типов SQLite и типов демоэкзамена

 Таблица соответствия

| Тип SQLite | Тип из демоэкзамена | Комментарий |
|------------|---------------------|-------------|
| INTEGER | INTEGER / INT | совпадает напрямую |
| TEXT | VARCHAR / NVARCHAR | строка произвольной длины |
| TEXT (ISO 8601) | DATE | дата хранится как строка |
| REAL | NUMERIC / DECIMAL | число с плавающей точкой |
| NUMERIC | NUMERIC / DECIMAL | число с фиксированной точностью |

 полей из задания 1.5

| Поле | Назначение | Тип SQLite | Тип из демоэкзамена |
|------|------------|------------|---------------------|
| А | Идентификатор пользователя | INTEGER | INTEGER |
| Б | Фамилия пользователя | TEXT | VARCHAR |
| В | Логин пользователя | TEXT | VARCHAR |
| Г | Дата заказа | TEXT (ISO 8601) | DATE |
| Д | Наименование товара | TEXT | VARCHAR |
| Е | Путь к изображению товара | TEXT | VARCHAR |
| Ж | Размер обуви | REAL | NUMERIC |
| З | Доступное количество | INTEGER | INTEGER |
| И | Цена товара | NUMERIC(10,2) | NUMERIC |
| К | Количество в заказе | INTEGER | INTEGER |
| Л | Цена позиции в заказе | NUMERIC(10,2) | NUMERIC |
| М | Идентификатор заказа | INTEGER | INTEGER |

 Краткая запись ответа

А — INTEGER (INTEGER);
Б — TEXT (VARCHAR);
В — TEXT (VARCHAR);
Г — TEXT ISO 8601 (DATE);
Д — TEXT (VARCHAR);
Е — TEXT (VARCHAR);
Ж — REAL (NUMERIC);
З — INTEGER (INTEGER);
И — NUMERIC (NUMERIC);
К — INTEGER (INTEGER);
Л — NUMERIC (NUMERIC);
М — INTEGER (INTEGER).