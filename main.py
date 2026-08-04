from models import ProductFactory, PhysicalProduct
from catalogue import Catalogue
from cart import ShoppingCartList, CartManager, AddItemCommand, RemoveItemCommand, UpdateQuantityCommand
from discounts import BaseOrder, FlatDiscount, PercentageDiscount, BuyOneGetOneFree
from shipping import ShippingFacade
from orders import Order, OrderProcessor


def ask(prompt, default):
    raw = input(f"{prompt} [{default}]: ").strip()
    return raw if raw else str(default)


def seed_catalogue() -> Catalogue:
    catalogue = Catalogue()
    catalogue.add_product(ProductFactory.create_product("Physical", "LPT-1", "Laptop", 1000.0, {"electronics", "sale"}, 2.5))
    catalogue.add_product(ProductFactory.create_product("Digital", "EBK-1", "Python Guide", 20.0, {"education", "digital"}))
    catalogue.add_product(ProductFactory.create_product("Subscription", "SUB-1", "Music Premium", 15.0, {"entertainment", "digital"}))
    catalogue.add_product(ProductFactory.create_product("Physical", "HPH-1", "Headphones", 80.0, {"electronics", "sale"}, 0.4))
    return catalogue


def print_products(products):
    if not products:
        print("No matching products.")
        return
    for p in products:
        print(f" - [{p.sku}] {p.name} ({type(p).__name__}) - ${p.price:.2f}, tax=${p.calculate_tax():.2f}, tags={sorted(p.tags)}")


def handle_add_product(catalogue):
    print("\n-- Add Product --")
    prod_type = ask("Type (Physical/Digital/Subscription)", "Physical")
    sku = input("SKU: ").strip()
    name = input("Name: ").strip()
    price = float(ask("Price", "0"))
    tags_raw = input("Tags (comma-separated): ").strip()
    tags = {t.strip() for t in tags_raw.split(",") if t.strip()}
    weight = float(ask("Weight (kg, physical only)", "0")) if prod_type.lower() == "physical" else 0.0
    try:
        product = ProductFactory.create_product(prod_type, sku, name, price, tags, weight)
        catalogue.add_product(product)
        print(f"Added {product}.")
    except ValueError as e:
        print(f"Error: {e}")


def handle_update_product(catalogue):
    print("\n-- Update Product --")
    sku = input("SKU to update: ").strip()
    product = catalogue.get_product(sku)
    if not product:
        print("Product not found.")
        return
    name = ask("Name", product.name)
    price = float(ask("Price", product.price))
    tags_raw = ask("Tags (comma-separated)", ",".join(sorted(product.tags)))
    tags = {t.strip() for t in tags_raw.split(",") if t.strip()}
    fields = {"name": name, "price": price, "tags": tags}
    if isinstance(product, PhysicalProduct):
        fields["weight"] = float(ask("Weight (kg)", product.weight))
    catalogue.update_product(sku, **fields)
    print("Updated.")


def handle_delete_product(catalogue):
    print("\n-- Delete Product --")
    sku = input("SKU to delete: ").strip()
    try:
        catalogue.remove_product(sku)
        print("Deleted.")
    except KeyError as e:
        print(e)


def handle_keyword_search(catalogue):
    print("\n-- Search by Keyword --")
    keyword = input("Keyword: ").strip()
    print_products(catalogue.search_by_keyword(keyword))


def handle_tag_search(catalogue):
    print("\n-- Search by Tags --")
    tags_raw = input("Tags to search (comma-separated): ").strip()
    tags = {t.strip() for t in tags_raw.split(",") if t.strip()}
    mode = ask("Match mode (all/any)", "all")
    print_products(catalogue.search_by_tags(tags, match_all=(mode.lower() != "any")))


def handle_add_to_cart(catalogue, cart, manager):
    print("\n-- Add Item to Cart --")
    sku = input("SKU to add: ").strip()
    product = catalogue.get_product(sku)
    if not product:
        print("Product not found.")
        return
    qty = int(ask("Quantity", "1"))
    manager.execute_command(AddItemCommand(cart, product, qty))
    print(f"Added {qty} x {product.name} to cart. Subtotal: ${cart.get_subtotal():.2f}")


def handle_remove_from_cart(cart, manager):
    print("\n-- Remove Item from Cart --")
    sku = input("SKU to remove: ").strip()
    qty_raw = input("Quantity to remove (blank = remove all): ").strip()
    qty = int(qty_raw) if qty_raw else None
    manager.execute_command(RemoveItemCommand(cart, sku, qty))
    print(f"Removed. Subtotal: ${cart.get_subtotal():.2f}")


def handle_update_cart_qty(cart, manager):
    print("\n-- Update Item Quantity --")
    sku = input("SKU: ").strip()
    new_qty = int(ask("New quantity", "1"))
    manager.execute_command(UpdateQuantityCommand(cart, sku, new_qty))
    print(f"Updated. Subtotal: ${cart.get_subtotal():.2f}")


def view_cart(cart):
    print("\n-- Cart Contents --")
    items = cart.to_list()
    if not items:
        print("Cart is empty.")
        return
    for item in items:
        print(f" - {item.product.name} x{item.quantity} = ${item.product.price * item.quantity:.2f}")
    print(f"Subtotal: ${cart.get_subtotal():.2f}")


def handle_checkout(cart, manager, processor):
    print("\n-- Checkout --")
    if cart.is_empty():
        print("Cart is empty, nothing to checkout.")
        return
    view_cart(cart)

    order = BaseOrder(cart.get_subtotal())

    if ask("Apply flat discount? (y/n)", "n").lower() == "y":
        amount = float(ask("Flat discount amount", "0"))
        order = FlatDiscount(order, amount)

    if ask("Apply percentage discount? (y/n)", "n").lower() == "y":
        pct = float(ask("Percentage (e.g. 10 for 10%)", "0"))
        order = PercentageDiscount(order, pct / 100)

    if ask("Apply Buy-One-Get-One-Free? (y/n)", "n").lower() == "y":
        item_prices = [item.product.price for item in cart.to_list() for _ in range(item.quantity)]
        order = BuyOneGetOneFree(order, item_prices)

    zone = ask("Shipping zone (Domestic/International)", "Domestic")
    shipping_cost = ShippingFacade.calculate_shipping(cart, zone)
    final_total = order.get_total() + shipping_cost

    print(f"\nDiscounted subtotal: ${order.get_total():.2f}")
    print(f"Shipping ({zone}): ${shipping_cost:.2f}")
    print(f"Final Total: ${final_total:.2f}")

    if ask("Submit this order? (y/n)", "y").lower() == "y":
        skus = [item.product.sku for item in cart.to_list()]
        new_order = Order(skus, final_total)
        processor.submit_order(new_order)
        cart.clear()
        manager.undo_stack.clear()
        manager.redo_stack.clear()


def print_menu():
    print("""
==================== E-Commerce Console ====================
 Catalogue:
  1. Add Product
  2. Update Product
  3. Delete Product
  4. Browse Products (sorted by price)
  5. Search by Keyword
  6. Search by Tags
 Cart:
  7. Add Item to Cart
  8. Remove Item from Cart
  9. Update Item Quantity
 10. View Cart
 11. Undo Last Cart Action
 12. Redo Last Cart Action
 Checkout:
 13. Checkout (discounts + shipping + submit order)
 14. Process Order Queue (fulfilment)
  0. Exit
==============================================================""")


def main():
    print("Welcome to the E-Commerce Console. Sample products have been pre-loaded.")
    catalogue = seed_catalogue()
    cart = ShoppingCartList()
    manager = CartManager(cart)
    processor = OrderProcessor()

    while True:
        print_menu()
        choice = input("Select an option: ").strip()
        print()

        if choice == "1":
            handle_add_product(catalogue)
        elif choice == "2":
            handle_update_product(catalogue)
        elif choice == "3":
            handle_delete_product(catalogue)
        elif choice == "4":
            print("Products sorted by price:")
            print_products(catalogue.sorted_list.to_list())
        elif choice == "5":
            handle_keyword_search(catalogue)
        elif choice == "6":
            handle_tag_search(catalogue)
        elif choice == "7":
            handle_add_to_cart(catalogue, cart, manager)
        elif choice == "8":
            handle_remove_from_cart(cart, manager)
        elif choice == "9":
            handle_update_cart_qty(cart, manager)
        elif choice == "10":
            view_cart(cart)
        elif choice == "11":
            print("Undone." if manager.undo() else "Nothing to undo.")
        elif choice == "12":
            print("Redone." if manager.redo() else "Nothing to redo.")
        elif choice == "13":
            handle_checkout(cart, manager, processor)
        elif choice == "14":
            print("-- Processing Order Queue --")
            if not processor.order_queue:
                print("No orders in queue.")
            else:
                processor.process_orders()
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid option.")
        print()


if __name__ == "__main__":
    main()
