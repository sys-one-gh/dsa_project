from abc import ABC, abstractmethod
from typing import Optional, List
from models import Product


class CartItem:
    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity
        self.next: Optional["CartItem"] = None


class ShoppingCartList:
    """Custom singly linked list representing the shopping cart."""

    def __init__(self):
        self.head: Optional[CartItem] = None

    def add(self, product: Product, qty: int):
        if qty <= 0:
            raise ValueError("Quantity must be positive.")
        current = self.head
        while current:
            if current.product.sku == product.sku:
                current.quantity += qty
                return
            current = current.next
        new_item = CartItem(product, qty)
        new_item.next = self.head
        self.head = new_item

    def remove(self, sku: str, qty: Optional[int] = None):
        """Remove `qty` units of sku (or the whole node if qty is None / >= current quantity)."""
        prev = None
        current = self.head
        while current:
            if current.product.sku == sku:
                if qty is None or qty >= current.quantity:
                    if prev:
                        prev.next = current.next
                    else:
                        self.head = current.next
                else:
                    current.quantity -= qty
                return
            prev, current = current, current.next

    def update_quantity(self, sku: str, new_qty: int):
        current = self.head
        while current:
            if current.product.sku == sku:
                if new_qty <= 0:
                    self.remove(sku)
                else:
                    current.quantity = new_qty
                return
            current = current.next

    def get_item(self, sku: str) -> Optional[CartItem]:
        current = self.head
        while current:
            if current.product.sku == sku:
                return current
            current = current.next
        return None

    def get_subtotal(self) -> float:
        total = 0.0
        current = self.head
        while current:
            total += current.product.price * current.quantity
            current = current.next
        return total

    def to_list(self) -> List[CartItem]:
        items = []
        current = self.head
        while current:
            items.append(current)
            current = current.next
        return items

    def is_empty(self) -> bool:
        return self.head is None

    def clear(self):
        self.head = None


# --- Command Pattern: enables undo / redo for cart edits ---
class ICartCommand(ABC):
    @abstractmethod
    def execute(self): ...

    @abstractmethod
    def undo(self): ...


class AddItemCommand(ICartCommand):
    def __init__(self, cart: ShoppingCartList, product: Product, qty: int):
        self.cart = cart
        self.product = product
        self.qty = qty

    def execute(self):
        self.cart.add(self.product, self.qty)

    def undo(self):
        self.cart.remove(self.product.sku, self.qty)


class RemoveItemCommand(ICartCommand):
    def __init__(self, cart: ShoppingCartList, sku: str, qty: Optional[int] = None):
        self.cart = cart
        self.sku = sku
        self.qty = qty
        self._removed_product: Optional[Product] = None
        self._removed_qty = 0

    def execute(self):
        item = self.cart.get_item(self.sku)
        if not item:
            return
        self._removed_product = item.product
        self._removed_qty = item.quantity if (self.qty is None or self.qty >= item.quantity) else self.qty
        self.cart.remove(self.sku, self.qty)

    def undo(self):
        if self._removed_product:
            self.cart.add(self._removed_product, self._removed_qty)


class UpdateQuantityCommand(ICartCommand):
    def __init__(self, cart: ShoppingCartList, sku: str, new_qty: int):
        self.cart = cart
        self.sku = sku
        self.new_qty = new_qty
        self._old_qty: Optional[int] = None

    def execute(self):
        item = self.cart.get_item(self.sku)
        self._old_qty = item.quantity if item else None
        self.cart.update_quantity(self.sku, self.new_qty)

    def undo(self):
        if self._old_qty is not None:
            self.cart.update_quantity(self.sku, self._old_qty)


class CartManager:
    """Manages undo / redo stacks of cart commands."""

    def __init__(self, cart: ShoppingCartList):
        self.cart = cart
        self.undo_stack: List[ICartCommand] = []
        self.redo_stack: List[ICartCommand] = []

    def execute_command(self, command: ICartCommand):
        command.execute()
        self.undo_stack.append(command)
        self.redo_stack.clear()

    def undo(self) -> bool:
        if not self.undo_stack:
            return False
        command = self.undo_stack.pop()
        command.undo()
        self.redo_stack.append(command)
        return True

    def redo(self) -> bool:
        if not self.redo_stack:
            return False
        command = self.redo_stack.pop()
        command.execute()
        self.undo_stack.append(command)
        return True
