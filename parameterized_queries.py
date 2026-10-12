# parameterized_queries.py
import psycopg

DSN = "postgresql://postgres:admin@localhost:5432/service_manager"


def demonstrate_sql_injection():
    """Показати різницю між небезпечним та безпечним кодом"""

    print("=== ПАРАМЕТРИЗОВАНІ ЗАПИТИ ===\n")

    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            # Створюємо таблицю users на випадок, якщо вона ще не була створена
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    email VARCHAR(150) UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT NOW()
                );
            """)
            conn.commit()

            # Очищуємо тестові записи перед запуском
            cur.execute(
                "DELETE FROM users WHERE username IN (%s, %s);",
                ("alice_wonderland", "bob_builder"),
            )
            conn.commit()

            # 1. Тестові дані
            print("1️⃣  Вставляємо тестові дані:\n")
            cur.execute(
                "INSERT INTO users (username, email) VALUES (%s, %s);",
                ("alice_wonderland", "alice@example.com"),
            )
            conn.commit()
            print("✅ Вставлено: alice_wonderland\n")

            # 2. Безпечний пошук
            print("2️⃣  БЕЗПЕЧНИЙ пошук за username:\n")
            search_username = "alice_wonderland"
            cur.execute(
                "SELECT id, username, email FROM users WHERE username = %s;",
                (search_username,),
            )
            result = cur.fetchone()
            if result:
                print(f"✅ Знайдено: {result}\n")

            # 3. Демонстрація небезпечного запиту
            print("3️⃣  НЕБЕЗПЕЧНИЙ код (для демонстрації):\n")
            print("❌ НІКОЛИ не робіть так:")
            dangerous_username = "admin'; DROP TABLE users; --"
            dangerous_query = (
                f"SELECT * FROM users WHERE username = '{dangerous_username}';"
            )
            print(f"   {dangerous_query}")
            print("   ^ Це видалить всю таблицю користувачів!\n")

            print("✅ ПРАВИЛЬНО з параметрами:")
            print("   cur.execute(")
            print('       "SELECT * FROM users WHERE username = %s;",')
            print(f"       ('{dangerous_username}',)")
            print("   )")
            print(
                "   ^ Шукає користувача з буквальною назвою, тому безпечно\n"
            )

            # 4. Приклад із кількома параметрами
            print("4️⃣  Приклад з кількома параметрами:\n")
            cur.execute(
                "INSERT INTO users (username, email) VALUES (%s, %s);",
                ("bob_builder", "bob@example.com"),
            )
            conn.commit()

            cur.execute(
                "UPDATE users SET email = %s WHERE username = %s;",
                ("bob.new@example.com", "bob_builder"),
            )
            conn.commit()
            print("✅ Оновлено: bob_builder → bob.new@example.com\n")

            cur.execute(
                "DELETE FROM users WHERE username = %s;", ("bob_builder",)
            )
            conn.commit()
            print("✅ Видалено: bob_builder\n")


if __name__ == "__main__":
    try:
        demonstrate_sql_injection()
    except psycopg.Error as e:
        print(f"❌ Помилка: {e}")