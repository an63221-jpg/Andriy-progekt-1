import pytest
from models import Customer, Part, Service, RepairOrder


# 1. ТЕСТИ ДЛЯ КЛАСУ CUSTOMER
def test_customer_creation():
    """Перевірка коректного створення клієнта."""
    customer = Customer("Іван", "+380671112233")
    assert customer.name == "Іван"
    assert customer.phone == "+380671112233"


def test_customer_empty_name_raises_error():
    """Перевірка винятку при порожньому імені клієнта."""
    with pytest.raises(ValueError):
        Customer(name="", phone="+380671112233")


# 2. ТЕСТИ ДЛЯ КЛАСУ PART
def test_part_creation(sample_part):
    """Перевірка атрибутів запчастини через fixture."""
    assert sample_part.name == "Гальмівні колодки"
    assert sample_part.price == 1200.0


def test_part_negative_price_raises_error():
    """Граничне значення: від'ємна ціна повинна викликати ValueError."""
    with pytest.raises(ValueError):
        Part(name="Фільтр", price=-150.0)


def test_part_zero_price():
    """Граничне значення: нульова ціна (наприклад, подарунок/акція)."""
    part = Part(name="Безкоштовна наліпка", price=0.0)
    assert part.price == 0.0


# 3. ТЕСТИ ДЛЯ КЛАСУ SERVICE
def test_service_creation(sample_service):
    """Перевірка атрибутів послуги."""
    assert sample_service.name == "Заміна колодок"
    assert sample_service.price == 600.0


def test_service_negative_price_raises_error():
    """Виняток для від'ємної вартості робіт."""
    with pytest.raises(ValueError):
        Service(name="Діагностика", price=-50.0)


# 4. ТЕСТИ ДЛЯ КЛАСУ REPAIRORDER
def test_empty_order_total_is_zero(empty_order):
    """Граничне значення: сума щойно створеного замовлення має дорівнювати 0."""
    assert empty_order.calculate_total() == 0.0
    assert len(empty_order.parts) == 0
    assert len(empty_order.services) == 0


def test_add_part_to_order(empty_order, sample_part):
    """Перевірка додавання деталі та перерахунку суми."""
    empty_order.add_part(sample_part)
    assert len(empty_order.parts) == 1
    assert empty_order.calculate_total() == 1200.0


def test_add_service_to_order(empty_order, sample_service):
    """Перевірка додавання послуги та перерахунку суми."""
    empty_order.add_service(sample_service)
    assert len(empty_order.services) == 1
    assert empty_order.calculate_total() == 600.0


def test_full_order_total(empty_order, sample_part, sample_service):
    """Перевірка повної калькуляції деталей + робіт."""
    empty_order.add_part(sample_part)
    empty_order.add_service(sample_service)
    # 1200.0 + 600.0 = 1800.0
    assert empty_order.calculate_total() == 1800.0


def test_order_status_progression(empty_order):
    """Перевірка зміни стану замовлення."""
    assert empty_order.status == "Open"
    empty_order.complete_order()
    assert empty_order.status == "Completed"