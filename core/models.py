class ServiceException(Exception):
    """Базовий клас винятків проєкту"""
    pass

class OutOfStockException(ServiceException):
    """Виникає при нестачі товарів на складі"""
    pass

class InvalidPriceException(ServiceException):
    """Виникає при некоректній ціні"""
    pass


class Customer:
    def __init__(self, customer_id: int, name: str, phone: str):
        self.id = customer_id
        self.name = name
        self.phone = phone

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone
        }

    def __repr__(self) -> str:
        return f"Customer({self.id}, '{self.name}')"


class Part:
    def __init__(self, part_id: int, name: str, sku: str, price: float, stock: int):
        if price < 0:
            raise InvalidPriceException("Ціна запчастини не може бути від'ємною")
        self.id = part_id
        self.name = name
        self.sku = sku
        self.price = price
        self.stock = stock

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "sku": self.sku,
            "price": self.price,
            "stock": self.stock
        }

    def __repr__(self) -> str:
        return f"Part('{self.name}', SKU: {self.sku}, Stock: {self.stock})"


class Service:
    def __init__(self, service_id: int, name: str, price: float):
        if price < 0:
            raise InvalidPriceException("Ціна послуги не може бути від'ємною")
        self.id = service_id
        self.name = name
        self.price = price

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price
        }

    def __repr__(self) -> str:
        return f"Service('{self.name}', {self.price} грн)"


class RepairOrder:
    def __init__(self, order_id: int, customer: Customer, vehicle_info: str):
        self.id = order_id
        self.customer = customer
        self.vehicle_info = vehicle_info
        self.parts: list[tuple[Part, int]] = []
        self.services: list[Service] = []
        self.status = "Принят"

    def add_part(self, part: Part, quantity: int = 1) -> None:
        if part.stock < quantity:
            raise OutOfStockException(
                f"Недостатньо '{part.name}' на складі! Запитали: {quantity}, у наявності: {part.stock}"
            )
        part.stock -= quantity
        self.parts.append((part, quantity))
        print(f"✅ Запчастину '{part.name}' ({quantity} шт.) додано.")

    def add_service(self, service: Service) -> None:
        self.services.append(service)
        print(f"✅ Послугу '{service.name}' додано.")

    def calculate_total(self) -> float:
        total_services = sum(s.price for s in self.services)
        total_parts = sum(part.price * qty for part, qty in self.parts)
        return total_services + total_parts

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "customer": self.customer.to_dict(),
            "vehicle_info": self.vehicle_info,
            "status": self.status,
            "services": [s.to_dict() for s in self.services],
            "parts": [
                {"part": p.to_dict(), "quantity": qty} 
                for p, qty in self.parts
            ],
            "total_price": self.calculate_total()
        }