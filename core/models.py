class Customer:
    def __init__(self, customer_id: int, name: str, phone: str):
        self.id = customer_id
        self.name = name
        self.phone = phone


class Part:
    def __init__(self, part_id: int, name: str, sku: str, price: float, stock: int):
        self.id = part_id
        self.name = name
        self.sku = sku
        self.price = price
        self.stock = stock


class Service:
    def __init__(self, service_id: int, name: str, price: float):
        self.id = service_id
        self.name = name
        self.price = price


class RepairOrder:
    def __init__(self, order_id: int, customer: Customer, vehicle_info: str):
        self.id = order_id
        self.customer = customer
        self.vehicle_info = vehicle_info
        self.parts = []
        self.services = []
        self.status = "Принят"

    def add_part(self, part: Part, quantity: int):
        if part.stock >= quantity:
            part.stock -= quantity
            self.parts.append((part, quantity))
            print(f"✅ Запчасть {part.name} ({quantity} шт.) добавлена.")
        else:
            print(f"❌ Нет {part.name} на складе! Доступно: {part.stock}")

    def add_service(self, service: Service):
        self.services.append(service)
        print(f"✅ Услуга '{service.name}' добавлена.")

    def calculate_total(self) -> float:
        total_services = sum(s.price for s in self.services)
        total_parts = sum(part.price * qty for part, qty in self.parts)
        return total_services + total_parts
