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