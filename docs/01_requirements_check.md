 Проверка соответствия требованиям

| Требование | Таблица | Поле | Операция |
| :--- | :--- | :--- | :--- |
| В каталоге должно храниться количество | `stock_items` | `available_quantity` | SELECT, UPDATE |
| Для каждой модели должно сохраняться изображение | `products` | `image_path` | SELECT |
| Пользователь должен выбирать одну или несколько пар | `order_items` | `quantity` | INSERT, UPDATE |
| Просмотр списка заказов (дата, ФИО) | `orders`, `users` | `order_date`, `last_name` | SELECT |
| Управление заказами | `orders` | `order_id` | INSERT, UPDATE, DELETE |

 Проверка ролей
*   **Неавторизованный:** Доступ к `products`, `stock_items` (SELECT).
*   **Авторизованный:** Доступ к `orders`, `order_items` (INSERT, UPDATE, DELETE).
*   **Менеджер:** Доступ к `orders` (SELECT, INSERT, DELETE).
*   **Администратор:** Доступ к `orders` (UPDATE).