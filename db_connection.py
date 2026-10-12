# db_connection.py
import psycopg

# Підключення з вашим новим паролем admin
DSN = "postgresql://postgres:admin@localhost:5432/lesson_30_test"

try:
    with psycopg.connect(DSN) as conn:
        print("✅ Успішно підключені до PostgreSQL!")

        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            version = cur.fetchone()[0]
            print(f"\n📊 PostgreSQL версія:\n{version}\n")

            cur.execute("SELECT current_user;")
            user = cur.fetchone()[0]
            print(f"👤 Користувач: {user}")

            cur.execute("SELECT current_database();")
            database = cur.fetchone()[0]
            print(f"📁 Поточна БД: {database}")

except psycopg.Error as e:
    print(f"❌ Помилка підключення: {e}")
