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