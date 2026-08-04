from abc import ABC, abstractmethod
from typing import List


# --- Decorator Pattern: layer discounts onto an order dynamically ---
class IOrder(ABC):
    @abstractmethod
    def get_total(self) -> float: ...


class BaseOrder(IOrder):
    def __init__(self, cart_subtotal: float):
        self.cart_subtotal = cart_subtotal

    def get_total(self) -> float:
        return self.cart_subtotal


class DiscountDecorator(IOrder):
    def __init__(self, order: IOrder):
        self.order = order

    @abstractmethod
    def get_total(self) -> float: ...


class FlatDiscount(DiscountDecorator):
    def __init__(self, order: IOrder, amount: float):
        super().__init__(order)
        self.amount = amount

    def get_total(self) -> float:
        return max(0.0, self.order.get_total() - self.amount)


class PercentageDiscount(DiscountDecorator):
    def __init__(self, order: IOrder, percentage: float):
        super().__init__(order)
        self.percentage = percentage

    def get_total(self) -> float:
        return self.order.get_total() * (1 - self.percentage)


class BuyOneGetOneFree(DiscountDecorator):
    """Makes the cheapest unit among `item_prices` free, if there are at least 2 units."""

    def __init__(self, order: IOrder, item_prices: List[float]):
        super().__init__(order)
        self.item_prices = item_prices

    def get_total(self) -> float:
        total = self.order.get_total()
        if len(self.item_prices) >= 2:
            total -= min(self.item_prices)
        return max(0.0, total)
