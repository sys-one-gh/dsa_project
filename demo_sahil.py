"""
Demo script for Sahil's part of the project: shipping.py (Facade pattern)
and orders.py (FIFO Queue).

Run:
    python3 demo_sahil.py
"""

from models import ProductFactory
from cart import ShoppingCartList
from shipping import ShippingFacade
from orders import Order, OrderProcessor


def rule(title=""):
    print()
    print("=" * 70)
    if title:
        print(title)
        print("=" * 70)


# ---------------------------------------------------------------------
# 1. Build some products via the Factory (Parth's module, used as input)
# ---------------------------------------------------------------------
laptop = ProductFactory.create_product("Physical", "SKU-100", "Laptop", 1200.00, {"electronics"}, weight=2.2)
headphones = ProductFactory.create_product("Physical", "SKU-101", "Headphones", 150.00, {"electronics"}, weight=0.3)
ebook = ProductFactory.create_product("Digital", "SKU-102", "Python Guide", 25.00, {"books"})

rule("SAHIL'S PART — SHIPPING (Facade pattern)")

cart = ShoppingCartList()
cart.add(laptop, 1)
cart.add(headphones, 2)
cart.add(ebook, 1)

print("\n[1] Cart contains 1x Laptop (2.2kg), 2x Headphones (0.3kg each), 1x e-book (0kg)")
print(f"    Total physical weight = {1 * 2.2 + 2 * 0.3:.2f}kg")

print("\n[2] ShippingFacade.calculate_shipping(cart, 'Domestic') -> ONE call,")
print("    hides weight calc + zone lookup + carrier-quote stub")
domestic = ShippingFacade.calculate_shipping(cart, "Domestic")
print(f"    Domestic shipping cost:      ${domestic:.2f}")

print("\n[3] Same cart, 'International' zone (1.5x multiplier)")
international = ShippingFacade.calculate_shipping(cart, "International")
print(f"    International shipping cost: ${international:.2f}")

print("\n[4] Digital-only cart contributes zero weight -> base rate only")
digital_cart = ShoppingCartList()
digital_cart.add(ebook, 5)
digital_only = ShippingFacade.calculate_shipping(digital_cart, "Domestic")
print(f"    5x e-books, shipping cost: ${digital_only:.2f} (base rate, 0kg)")

rule("ORDER FULFILMENT — FIFO QUEUE (orders.py)")

processor = OrderProcessor()

print("\n[5] Submit three orders, in this order: A, B, C")
order_a = Order(["SKU-100"], final_total=1200.00 + domestic)
order_b = Order(["SKU-101", "SKU-101"], final_total=300.00 + domestic)
order_c = Order(["SKU-102"], final_total=25.00 + domestic)
processor.submit_order(order_a)
processor.submit_order(order_b)
processor.submit_order(order_c)

print(f"\nQueue has {len(processor.order_queue)} pending orders, history has {len(processor.order_history)}")

print("\n[6] process_orders() drains the ENTIRE queue, front to back (FIFO)")
processor.process_orders()

print("\n[7] order_history now holds every order, in the exact order submitted:")
for order in processor.order_history:
    print(f"    {order}")

print(f"\nQueue has {len(processor.order_queue)} pending orders left (should be 0)")

rule("END OF DEMO — Sahil's slice (shipping.py + orders.py)")
print()
