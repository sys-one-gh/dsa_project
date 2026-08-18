"""
Demo script for Dhruv's part of the project: cart.py (custom linked list +
Command pattern + two Stacks) and discounts.py (Decorator pattern).

Run:
    python3 demo_dhruv.py
"""

from models import ProductFactory
from cart import ShoppingCartList, CartManager, AddItemCommand, RemoveItemCommand, UpdateQuantityCommand
from discounts import BaseOrder, FlatDiscount, PercentageDiscount, BuyOneGetOneFree


def rule(title=""):
    print()
    print("=" * 70)
    if title:
        print(title)
        print("=" * 70)


def show_cart(cart: ShoppingCartList):
    items = cart.to_list()
    if not items:
        print("  (cart is empty)")
        return
    for item in items:
        print(f"  - {item.product.name:<20} x{item.quantity:<3} "
              f"@ ${item.product.price:>7.2f}  = ${item.product.price * item.quantity:>8.2f}")
    print(f"  {'SUBTOTAL':<20}      {'':<12}  ${cart.get_subtotal():>8.2f}")


# ---------------------------------------------------------------------
# 1. Build some products via the Factory (Parth's module, used as input)
# ---------------------------------------------------------------------
laptop = ProductFactory.create_product("Physical", "SKU-100", "Laptop", 1200.00, {"electronics"}, weight=2.2)
headphones = ProductFactory.create_product("Physical", "SKU-101", "Headphones", 150.00, {"electronics", "sale"}, weight=0.3)
ebook = ProductFactory.create_product("Digital", "SKU-102", "Python Guide", 25.00, {"books"})

cart = ShoppingCartList()
manager = CartManager(cart)

rule("DHRUV'S PART — CART (custom linked list + Command pattern)")

print("\n[1] Add 1x Laptop, 2x Headphones, 1x Python Guide via AddItemCommand")
manager.execute_command(AddItemCommand(cart, laptop, 1))
manager.execute_command(AddItemCommand(cart, headphones, 2))
manager.execute_command(AddItemCommand(cart, ebook, 1))
show_cart(cart)

print("\n[2] Add 1 more Headphones (same SKU merges into the existing node)")
manager.execute_command(AddItemCommand(cart, headphones, 1))
show_cart(cart)

print("\n[3] Update Headphones quantity to 1 via UpdateQuantityCommand")
manager.execute_command(UpdateQuantityCommand(cart, "SKU-101", 1))
show_cart(cart)

print("\n[4] Remove the Python Guide via RemoveItemCommand")
manager.execute_command(RemoveItemCommand(cart, "SKU-102"))
show_cart(cart)

rule("UNDO / REDO — two Stacks (undo_stack / redo_stack)")

print(f"\nundo_stack has {len(manager.undo_stack)} commands, redo_stack has {len(manager.redo_stack)}")

print("\n[5] Undo (reverses the RemoveItemCommand -> Python Guide comes back)")
manager.undo()
show_cart(cart)

print("\n[6] Undo again (reverses the UpdateQuantityCommand -> Headphones back to 3)")
manager.undo()
show_cart(cart)

print(f"\nundo_stack now has {len(manager.undo_stack)} commands, redo_stack has {len(manager.redo_stack)}")

print("\n[7] Redo (re-applies the UpdateQuantityCommand -> Headphones back to 1)")
manager.redo()
show_cart(cart)

print("\n[8] New edit after an undo clears the redo stack (can't redo into a stale future)")
manager.execute_command(UpdateQuantityCommand(cart, "SKU-101", 2))
print(f"redo_stack length after a fresh command: {len(manager.redo_stack)}")
show_cart(cart)

rule("CHECKOUT — DECORATOR PATTERN (discounts.py)")

subtotal = cart.get_subtotal()
print(f"\nCart subtotal (BaseOrder): ${subtotal:.2f}")

order = BaseOrder(subtotal)
print(f"[BaseOrder]                                total = ${order.get_total():.2f}")

order = FlatDiscount(order, 50.00)
print(f"[+ FlatDiscount($50)]                      total = ${order.get_total():.2f}")

order = PercentageDiscount(order, 0.10)
print(f"[+ PercentageDiscount(10%)]                 total = ${order.get_total():.2f}")

item_prices = [item.product.price for item in cart.to_list() for _ in range(item.quantity)]
order = BuyOneGetOneFree(order, item_prices)
print(f"[+ BuyOneGetOneFree(cheapest unit free)]    total = ${order.get_total():.2f}")

rule("END OF DEMO — Dhruv's slice (cart.py + discounts.py)")
print()
