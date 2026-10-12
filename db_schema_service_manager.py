# db_schema_service_manager.py
import psycopg

ROOT_DSN = "postgresql://postgres:admin@localhost:5432/template1"
DB_DSN = "postgresql://postgres:admin@localhost:5432/service_manager"


def create_database():
    """Створити БД для Service Management System та її таблиці."""
    try:
        # Крок 1: Підключення до template1 та створення бази service_manager
        conn = psycopg.connect(ROOT_DSN)
        conn.autocommit = True

        with conn.cursor() as cur:
            cur.execute("DROP DATABASE IF EXISTS service_manager;")
            cur.execute("CREATE DATABASE service_manager;")

        conn.close()
        print("✅ База даних service_manager створена")

        # Крок 2: Підключення до нової БД і створення таблиць
        with psycopg.connect(DB_DSN) as conn:
            with conn.cursor() as cur:

                # 1. Клієнти
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS clients (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(150) NOT NULL,
                        phone VARCHAR(20),
                        email VARCHAR(100),
                        created_at TIMESTAMP DEFAULT NOW()
                    );
                """)

                # 2. Послуги
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS services (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(150) NOT NULL,
                        description TEXT,
                        price DECIMAL(10, 2) NOT NULL,
                        duration_minutes INTEGER,
                        created_at TIMESTAMP DEFAULT NOW()
                    );
                """)

                # 3. Замовлення (зв'язки FOREIGN KEY)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS orders (
                        id SERIAL PRIMARY KEY,
                        client_id INTEGER NOT NULL,
                        service_id INTEGER NOT NULL,
                        order_date DATE NOT NULL,
                        status VARCHAR(50) DEFAULT 'created',
                        total_price DECIMAL(10, 2) NOT NULL,
                        notes TEXT,
                        created_at TIMESTAMP DEFAULT NOW(),
                        FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE,
                        FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE RESTRICT
                    );
                """)

                # 4. Інвентар / запчастини
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS inventory (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(150) NOT NULL,
                        quantity INTEGER NOT NULL,
                        unit_price DECIMAL(10, 2),
                        min_quantity INTEGER DEFAULT 0,
                        created_at TIMESTAMP DEFAULT NOW()
                    );
                """)

                conn.commit()
                print(
                    "✅ Таблиці створені: clients, services, orders, inventory"
                )

                # Перевірка списку таблиць
                cur.execute("""
                    SELECT table_name FROM information_schema.tables 
                    WHERE table_schema = 'public';
                """)
                tables = cur.fetchall()
                table_names = ", ".join([t[0] for t in tables])
                print(f"\n📊 Таблиці в БД: {table_names}")

    except psycopg.Error as e:
        print(f"❌ Помилка: {e}")


if __name__ == "__main__":
    create_database()