from models import Customer, Part, Service, RepairOrder
def main():
    print("=== Auto Service CRM запущен отдельно ===")
    
    # Создаем тестовые данные
    client = Customer(1, "Андрей", "+380970000000")
    filter_part = Part(101, "Фильтр воздуха", "AF-44", 350.0, 10)
    repair_job = Service(1, "Замена воздушного фильтра", 150.0)

    # Оформляем заказ
    order = RepairOrder(1, client, "Skoda Octavia")
    order.add_service(repair_job)
    order.add_part(filter_part, 1)
    
    print("\n" + "="*30)
    print(f"Заказ №{order.id} для: {order.customer.name}")
    print(f"Итого к оплате: {order.calculate_total()} грн.")
    print("="*30)

if __name__ == "__main__":
    main()