# crud_operations.py
from dataclasses import dataclass
from typing import List, Optional
import psycopg

DSN = "postgresql://postgres:admin@localhost:5432/service_manager"


@dataclass
class User:
    id: int
    username: str
    email: str


class UserRepository:
    """Репозиторій для роботи з користувачами"""

    def __init__(self, dsn: str):
        self.dsn = dsn
        self._ensure_table_exists()

    def _ensure_table_exists(self):
        """Створити таблицю users, якщо вона відсутня"""
        with psycopg.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(100) UNIQUE NOT NULL,
                        email VARCHAR(150) UNIQUE NOT NULL,
                        created_at TIMESTAMP DEFAULT NOW()
                    );
                """)
                conn.commit()

    def create(self, username: str, email: str) -> Optional[int]:
        """Створити користувача, повернути ID"""
        with psycopg.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(
                        "INSERT INTO users (username, email) VALUES (%s, %s) RETURNING id;",
                        (username, email),
                    )
                    user_id = cur.fetchone()[0]
                    conn.commit()
                    return user_id
                except psycopg.IntegrityError:
                    print(
                        f"❌ Помилка: користувач {username} або {email} вже існує"
                    )
                    return None

    def read(self, user_id: int) -> Optional[User]:
        """Отримати користувача по ID"""
        with psycopg.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, username, email FROM users WHERE id = %s;",
                    (user_id,),
                )
                row = cur.fetchone()
                if row:
                    return User(*row)
                return None

    def read_all(self) -> List[User]:
        """Отримати всіх користувачів"""
        with psycopg.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, username, email FROM users ORDER BY id;"
                )
                return [User(*row) for row in cur.fetchall()]

    def update(
        self,
        user_id: int,
        username: Optional[str] = None,
        email: Optional[str] = None,
    ) -> bool:
        """Оновити дані користувача"""
        with psycopg.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                if username and email:
                    cur.execute(
                        "UPDATE users SET username = %s, email = %s WHERE id = %s;",
                        (username, email, user_id),
                    )
                elif username:
                    cur.execute(
                        "UPDATE users SET username = %s WHERE id = %s;",
                        (username, user_id),
                    )
                elif email:
                    cur.execute(
                        "UPDATE users SET email = %s WHERE id = %s;",
                        (email, user_id),
                    )
                else:
                    return False

                conn.commit()
                return cur.rowcount > 0

    def delete(self, user_id: int) -> bool:
        """Видалити користувача"""
        with psycopg.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
                conn.commit()
                return cur.rowcount > 0


if __name__ == "__main__":
    repo = UserRepository(DSN)

    print("=== CRUD ОПЕРАЦІЇ ===\n")

    # CREATE
    print("📝 CREATE — додавання користувачів:")
    user_id_1 = repo.create("ivan_petrov", "ivan@example.com")
    user_id_2 = repo.create("maria_sidorenko", "maria@example.com")
    print(f"✅ Користувачі створені: ID {user_id_1}, {user_id_2}\n")

    # READ ONE
    print("📖 READ — отримання користувача:")
    user = repo.read(user_id_1)
    if user:
        print(f"✅ {user.username}: {user.email}\n")

    # READ ALL
    print("📚 READ ALL — отримання всіх користувачів:")
    users = repo.read_all()
    for u in users:
        print(f"  - {u.username} ({u.email})")
    print()

    # UPDATE
    print("✏️ UPDATE — оновлення користувача:")
    success = repo.update(user_id_1, email="newemail@example.com")
    if success:
        print("✅ Користувач оновлений\n")

    # DELETE
    print("🗑️ DELETE — видалення користувача:")
    success = repo.delete(user_id_2)
    if success:
        print("✅ Користувач видалений\n")

    # Фінальний список
    print("📊 Фінальний список користувачів:")
    users = repo.read_all()
    for u in users:
        print(f"  - {u.username} ({u.email})")