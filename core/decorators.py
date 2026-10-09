import functools
import inspect
import logging
import time

# Налаштування логування
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("service_manager.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)


def log_action(func):
    """Логує операції над сутностями системи (замовлення, клієнти, послуги)."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()

        result = func(*args, **kwargs)

        end_time = time.perf_counter()
        execution_time_ms = (end_time - start_time) * 1000

        # Збираємо аргументи без self
        args_to_log = args[1:] if args and hasattr(args[0], "__class__") else args
        args_repr = [repr(a) for a in args_to_log]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        all_args_str = ", ".join(args_repr + kwargs_repr)

        logging.info(
            f"[ДІЯ] {func.__name__} | ({all_args_str}) | {execution_time_ms:.1f} мс"
        )
        return result

    return wrapper


def validate_price(func):
    """Перевіряє аргумент price: int або float >= 0."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        bound_args = sig.bind_partial(*args, **kwargs)
        bound_args.apply_defaults()

        price = bound_args.arguments.get("price")

        if price is not None:
            if not isinstance(price, (int, float)) or price < 0:
                logging.warning(
                    f"validate_price: ціна має бути >= 0, отримано: {price}"
                )
                return None

        return func(*args, **kwargs)

    return wrapper


def notify_client(func):
    """ЗАГЛУШКА — буде реалізовано у Занятті 25 (HTTP + Telegram Bot API)."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        logging.debug(
            f"[notify_client] Сповіщення клієнта після {func.__name__}: "
            f"ще не реалізовано (Заняття 25)"
        )
        return result

    return wrapper


def memoize(func):
    """Бонус: кешує результати виконання функції."""
    cache = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key in cache:
            logging.debug(
                f"Кеш: повертаю збережений результат для {func.__name__}{args}"
            )
            return cache[key]

        result = func(*args, **kwargs)
        cache[key] = result
        return result

    return wrapper