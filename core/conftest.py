import pytest
from models import Customer, Part, Service, RepairOrder


@pytest.fixture
def sample_customer():
    """Фікстура для клієнта автосервісу."""
    return Customer(name="Андрій", phone="+380501234567")


@pytest.fixture
def sample_part():
    """Фікстура для автозапчастини."""
    return Part(name="Гальмівні колодки", price=1200.0)


@pytest.fixture
def sample_service():
    """Фікстура для послуги сервісу."""
    return Service(name="Заміна колодок", price=600.0)


@pytest.fixture
def empty_order(sample_customer):
    """Фікстура порожнього замовлення-наряду."""
    return RepairOrder(customer=sample_customer, car_model="Volkswagen Golf")