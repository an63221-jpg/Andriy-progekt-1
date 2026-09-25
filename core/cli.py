import argparse
from enum import Enum


class OrderStatus(Enum):
    CREATED = "Created"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class ReportPeriod(Enum):
    TODAY = "today"
    WEEK = "week"
    MONTH = "month"
    ALL = "all"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="service-manager",
        description="Service Management System — CRM для сервісу або клініки",
        epilog="Приклад: python main.py order create --client-id 1 --service-id 2",
    )
    parser.add_argument(
        "--version", action="version", version="Service Manager v0.3.0"
    )

    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")
    subparsers.required = True

    client_parser = subparsers.add_parser("client", help="Керування клієнтами")
    client_sub = client_parser.add_subparsers(
        dest="client_command", metavar="SUBCOMMAND"
    )
    client_sub.required = True

    client_add = client_sub.add_parser("add", help="Додати клієнта")
    client_add.add_argument("--name", required=True, help="Повне ім'я")
    client_add.add_argument("--phone", required=True, help="Номер телефону")
    client_add.add_argument("--email", default="", help="Email (необов'язково)")
    client_add.add_argument("--notes", default="", help="Нотатки")

    client_sub.add_parser("list", help="Список клієнтів")

    client_show = client_sub.add_parser("show", help="Деталі клієнта")
    client_show.add_argument("--id", type=int, required=True, help="ID клієнта")

    service_parser = subparsers.add_parser("service", help="Каталог послуг")
    service_sub = service_parser.add_subparsers(
        dest="service_command", metavar="SUBCOMMAND"
    )
    service_sub.required = True

    service_add = service_sub.add_parser("add", help="Додати послугу")
    service_add.add_argument("--name", required=True, help="Назва послуги")
    service_add.add_argument(
        "--price", type=float, required=True, help="Вартість (грн)"
    )
    service_add.add_argument(
        "--duration", type=int, default=60, help="Тривалість (хв)"
    )

    service_sub.add_parser("list", help="Список послуг")

    order_parser = subparsers.add_parser("order", help="Замовлення / записи")
    order_sub = order_parser.add_subparsers(
        dest="order_command", metavar="SUBCOMMAND"
    )
    order_sub.required = True

    order_create = order_sub.add_parser("create", help="Створити замовлення")
    order_create.add_argument(
        "--client-id", type=int, required=True, help="ID клієнта"
    )
    order_create.add_argument(
        "--service-id", type=int, required=True, help="ID послуги"
    )
    order_create.add_argument("--notes", default="", help="Нотатки")
    order_create.add_argument(
        "--scheduled-at", default="", help="Дата і час запису"
    )

    order_list = order_sub.add_parser("list", help="Список замовлень")
    order_list.add_argument(
        "--status",
        choices=[s.value for s in OrderStatus],
        help="Фільтр за статусом",
    )
    order_list.add_argument("--client-id", type=int, help="Фільтр за клієнтом")

    order_status = order_sub.add_parser("status", help="Змінити статус")
    order_status.add_argument(
        "--id", type=int, required=True, help="ID замовлення"
    )
    order_status.add_argument(
        "--status",
        choices=[s.value for s in OrderStatus],
        required=True,
        help="Новий статус",
    )

    order_delete = order_sub.add_parser("delete", help="Видалити замовлення")
    order_delete.add_argument("--id", type=int, required=True)

    report_parser = subparsers.add_parser("report", help="Звіт по замовленнях")
    report_parser.add_argument(
        "--period",
        choices=[p.value for p in ReportPeriod],
        default=ReportPeriod.MONTH.value,
        help="Період (за замовчуванням: month)",
    )

    export_parser = subparsers.add_parser("export", help="Експорт даних")
    export_parser.add_argument(
        "--format", choices=["csv", "json"], default="csv"
    )

    return parser