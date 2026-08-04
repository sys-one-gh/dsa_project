from abc import ABC, abstractmethod
from typing import Set


class Product(ABC):
    def __init__(self, sku: str, name: str, price: float, tags: Set[str]):
        self.sku = sku
        self.name = name
        self.price = price
        self.tags = set(tags)

    @abstractmethod
    def calculate_tax(self) -> float: ...

    def get_weight(self) -> float:
        return 0.0

    def __repr__(self):
        return f"{self.__class__.__name__}({self.sku}, {self.name}, ${self.price:.2f})"


class PhysicalProduct(Product):
    def __init__(self, sku: str, name: str, price: float, tags: Set[str], weight: float):
        super().__init__(sku, name, price, tags)
        self.weight = weight

    def calculate_tax(self) -> float:
        return self.price * 0.13

    def get_weight(self) -> float:
        return self.weight


class DigitalProduct(Product):
    def calculate_tax(self) -> float:
        return self.price * 0.05


class SubscriptionProduct(Product):
    def calculate_tax(self) -> float:
        return 0.0


class ProductFactory:
    """Factory Method: instantiates the correct Product subtype from input."""

    @staticmethod
    def create_product(prod_type: str, sku: str, name: str, price: float, tags: Set[str], weight: float = 0.0) -> Product:
        prod_type_lower = prod_type.strip().lower()
        if prod_type_lower == "physical":
            return PhysicalProduct(sku, name, price, tags, weight)
        elif prod_type_lower == "digital":
            return DigitalProduct(sku, name, price, tags)
        elif prod_type_lower == "subscription":
            return SubscriptionProduct(sku, name, price, tags)
        raise ValueError(f"Unknown product type: {prod_type}")
