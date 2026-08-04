from typing import Dict, Set, List, Optional
from models import Product


class SortedNode:
    def __init__(self, product: Product):
        self.product = product
        self.next: Optional["SortedNode"] = None


class SortedLinkedList:
    """Maintains a linked list of products sorted ascending by price."""

    def __init__(self):
        self.head: Optional[SortedNode] = None

    def insert(self, product: Product):
        new_node = SortedNode(product)
        if not self.head or self.head.product.price >= product.price:
            new_node.next = self.head
            self.head = new_node
            return
        current = self.head
        while current.next and current.next.product.price < product.price:
            current = current.next
        new_node.next = current.next
        current.next = new_node

    def remove(self, sku: str):
        if not self.head:
            return
        if self.head.product.sku == sku:
            self.head = self.head.next
            return
        current = self.head
        while current.next:
            if current.next.product.sku == sku:
                current.next = current.next.next
                return
            current = current.next

    def to_list(self) -> List[Product]:
        result = []
        current = self.head
        while current:
            result.append(current.product)
            current = current.next
        return result


class Catalogue:
    """Product catalogue: Dictionary keyed by SKU + sorted linked list for price browsing."""

    def __init__(self):
        self.products: Dict[str, Product] = {}
        self.sorted_list = SortedLinkedList()

    # --- CRUD ---
    def add_product(self, product: Product):
        if product.sku in self.products:
            raise ValueError(f"SKU '{product.sku}' already exists.")
        self.products[product.sku] = product
        self.sorted_list.insert(product)

    def get_product(self, sku: str) -> Optional[Product]:
        return self.products.get(sku)

    def update_product(self, sku: str, **fields) -> Product:
        product = self.products.get(sku)
        if not product:
            raise KeyError(f"SKU '{sku}' not found.")
        price_changed = "price" in fields and fields["price"] is not None and fields["price"] != product.price
        for key, value in fields.items():
            if value is not None and hasattr(product, key):
                setattr(product, key, value)
        if price_changed:
            self.sorted_list.remove(sku)
            self.sorted_list.insert(product)
        return product

    def remove_product(self, sku: str):
        if sku not in self.products:
            raise KeyError(f"SKU '{sku}' not found.")
        del self.products[sku]
        self.sorted_list.remove(sku)

    # --- Search ---
    def search_by_keyword(self, keyword: str) -> List[Product]:
        keyword_lower = keyword.lower()
        return [p for p in self.products.values() if keyword_lower in p.name.lower()]

    def search_by_tags(self, tags: Set[str], match_all: bool = True) -> List[Product]:
        """match_all=True -> intersection (product must have ALL tags).
        match_all=False -> union-style match (product has ANY of the tags)."""
        if match_all:
            return [p for p in self.products.values() if tags.issubset(p.tags)]
        return [p for p in self.products.values() if tags & p.tags]

    def all_tags(self) -> Set[str]:
        result: Set[str] = set()
        for p in self.products.values():
            result |= p.tags
        return result
