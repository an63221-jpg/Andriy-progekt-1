from models import (
    Customer, 
    Part, 
    Service, 
    RepairOrder, 
    OutOfStockException, 
    InvalidPriceException
)

def main():
    print("=== Auto Service CRM запущено успішно ===")
    
    try:
        # 1. Створюємо тестові дані
        client = Customer(1, "Андрій", "+380970000000")
        filter_part = Part(101, "Фільтр повітря", "AF-44", 350.0, stock=10)
        repair_job = Service(1, "Заміна повітряного фільтра", 150.0)

        # 2. Оформлюємо замовлення
        order = RepairOrder(1, client, "Skoda Octavia")
        
        # 3. Додаємо послугу та запчастину
        order.add_service(repair_job)
        order.add_part(filter_part, quantity=1)

        # 4. Виводимо підсумок
        print("\n" + "="*35)
        print(f"Замовлення №{order.id} для: {order.customer.name}")
        print(f"Автомобіль: {order.vehicle_info}")
        print(f"Статус: {order.status}")
        print(f"Разом до сплати: {order.calculate_total()} грн.")
        print("="*35)

    except OutOfStockException as e:
        print(f"\n Помилка складу: {e}")
    except InvalidPriceException as e:
        print(f"\n Помилка ціни: {e}")
    except Exception as e:
        print(f"\n Непередбачена помилка: {e}")

if __name__ == "__main__":
    main()
    #19/08/26/#
    import time
from decorators import log_action, memoize, notify_client, validate_price


class ServiceManager:

    def __init__(self):
        self.orders = {}
        self.services = []
        self.parts = []
        self.next_order_id = 1

    @log_action
    @validate_price
    def create_order(self, client_name, service_name, price):
        order_id = self.next_order_id
        self.orders[order_id] = {
            "client": client_name,
            "service": service_name,
            "price": price,
            "status": "New",
        }
        self.next_order_id += 1
        return order_id

    @log_action
    @notify_client
    def update_status(self, order_id, new_status):
        if order_id in self.orders:
            self.orders[order_id]["status"] = new_status
            return True
        return False

    @log_action
    def delete_order(self, order_id):
        return self.orders.pop(order_id, None)

    @log_action
    @validate_price
    def add_service(self, service_name, price):
        self.services.append({"name": service_name, "price": price})
        return True

    @log_action
    @validate_price
    def add_part(self, part_name, price):
        self.parts.append({"name": part_name, "price": price})
        return True


# Тестовий запуск
if __name__ == "__main__":
    manager = ServiceManager()

    print("--- 1. Створення замовлень ---")
    manager.create_order("Іваненко", "Заміна масла", 800)
    manager.create_order("Петренко", "Діагностика підвіски", -50)

    print("\n--- 2. Оновлення статусу ---")
    manager.update_status(1, "Completed")

    print("\n--- 3. Видалення замовлення ---")
    manager.delete_order(1)

    #HW3
    from datetime import datetime
from functools import reduce
from models import Client, Order, OrderStatus, Service

c1 = Client(name="Іваненко", phone="+380991234567")
c2 = Client(name="Петренко", phone="+380679876543")
c3 = Client(name="Сидоренко", phone="+380501112233")
c4 = Client(name="Коваленко", phone="+380634445566")

s1 = Service(name="Заміна масла", price=800.0, duration_minutes=30)
s2 = Service(
    name="Діагностика підвіски", price=500.0, duration_minutes=45
)
s3 = Service(
    name="Заміна гальмівних колодок", price=1200.0, duration_minutes=60
)
s4 = Service(
    name="Комп'ютерна діагностика", price=600.0, duration_minutes=30
)

orders: list[Order] = [
    Order(
        client=c1,
        service=s1,
        status=OrderStatus.COMPLETED,
        created_at=datetime(2026, 3, 15, 10, 30),
    ),
    Order(
        client=c2,
        service=s2,
        status=OrderStatus.IN_PROGRESS,
        created_at=datetime(2026, 3, 15, 11, 00),
    ),
    Order(
        client=c3,
        service=s3,
        status=OrderStatus.COMPLETED,
        created_at=datetime(2026, 3, 14, 16, 45),
    ),
    Order(
        client=c1,
        service=s4,
        status=OrderStatus.CREATED,
        created_at=datetime(2026, 3, 16, 9, 15),
    ),
    Order(
        client=c4,
        service=s1,
        status=OrderStatus.CANCELLED,
        created_at=datetime(2026, 3, 13, 14, 20),
    ),
    Order(
        client=c2,
        service=s3,
        status=OrderStatus.COMPLETED,
        created_at=datetime(2026, 3, 16, 12, 00),
    ),
    Order(
        client=c3,
        service=s2,
        status=OrderStatus.IN_PROGRESS,
        created_at=datetime(2026, 3, 16, 14, 10),
    ),
]

active = list(filter(lambda o: o.is_active(), orders))
completed = list(
    filter(lambda o: o.status == OrderStatus.COMPLETED, orders)
)

total_revenue = reduce(
    lambda acc, o: acc + o.total_price(), completed, 0.0
)

active_summaries = list(map(lambda o: o.summary(), active))

sorted_completed = sorted(
    completed, key=lambda o: o.created_at, reverse=True
)

target_client = "Іваненко"
client_orders = list(
    filter(lambda o: o.client.name == target_client, orders)
)

print(f"Активних замовлень:     {len(active)}")
print(f"Завершених замовлень:  {len(completed)}")
print(f"Загальна виручка:      {total_revenue:.2f} грн")

print("\n--- Список активних замовлень ---")
for summary in active_summaries:
    print(summary)

print(f"\n--- Замовлення клієнта {target_client} ---")
for order in client_orders:
    print(order.summary())