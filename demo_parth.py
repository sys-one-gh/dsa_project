"""
Demo script for Parth's part of the project: models.py (Product hierarchy +
Factory Method) and catalogue.py (Dictionary + HashSet + Sorted Linked List).

Run:
    python3 demo_parth.py
"""

from models import ProductFactory
from catalogue import Catalogue


def rule(title=""):
    print()
    print("=" * 70)
    if title:
        print(title)
        print("=" * 70)


def show_sorted(catalogue: Catalogue):
    for p in catalogue.sorted_list.to_list():
        print(f"  - {p.name:<15} ${p.price:>8.2f}  tags={sorted(p.tags)}")


rule("PARTH'S PART — PRODUCT HIERARCHY + FACTORY METHOD (models.py)")

print("\n[1] ProductFactory builds the correct subclass from a type string")
laptop = ProductFactory.create_product("Physical", "SKU-100", "Laptop", 1200.00, {"electronics", "sale"}, weight=2.2)
ebook = ProductFactory.create_product("Digital", "SKU-101", "Python Guide", 25.00, {"books", "digital"})
plan = ProductFactory.create_product("Subscription", "SKU-102", "Music Premium", 15.00, {"entertainment", "digital"})

for p in (laptop, ebook, plan):
    print(f"  {p!r:<55} tax=${p.calculate_tax():>6.2f}  weight={p.get_weight()}kg")

print("\n[2] Unknown product type raises ValueError instead of failing silently")
try:
    ProductFactory.create_product("Bogus", "SKU-999", "X", 1.00, set())
except ValueError as e:
    print(f"    Caught expected error: {e}")

rule("CATALOGUE — DICTIONARY + HASHSET + SORTED LINKED LIST (catalogue.py)")

catalogue = Catalogue()
headphones = ProductFactory.create_product("Physical", "SKU-103", "Headphones", 150.00, {"electronics"}, weight=0.3)

print("\n[3] add_product() -> stored in Dictionary AND inserted into sorted linked list")
for p in (laptop, ebook, plan, headphones):
    catalogue.add_product(p)
print("Catalogue sorted by price (ascending):")
show_sorted(catalogue)

print("\n[4] get_product('SKU-100') -> O(1) Dictionary lookup by SKU")
print(f"    {catalogue.get_product('SKU-100')!r}")

print("\n[5] update_product('SKU-102', price=5000.00) re-sorts the linked list")
catalogue.update_product("SKU-102", price=5000.00)
show_sorted(catalogue)

print("\n[6] remove_product('SKU-101') deletes from BOTH the dict and sorted list")
catalogue.remove_product("SKU-101")
show_sorted(catalogue)

print("\n[7] search_by_keyword('phone') -> case-insensitive substring match")
for p in catalogue.search_by_keyword("phone"):
    print(f"    {p!r}")

print("\n[8] search_by_tags({'digital'}, match_all=True) -> HashSet INTERSECTION")
for p in catalogue.search_by_tags({"digital"}, match_all=True):
    print(f"    {p!r}")

print("\n[9] search_by_tags({'sale', 'entertainment'}, match_all=False) -> HashSet ANY-match")
for p in catalogue.search_by_tags({"sale", "entertainment"}, match_all=False):
    print(f"    {p!r}")

print("\n[10] all_tags() -> HashSet UNION of every product's tags")
print(f"     {sorted(catalogue.all_tags())}")

rule("END OF DEMO — Parth's slice (models.py + catalogue.py)")
print()
