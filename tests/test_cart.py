import unittest
from models import ProductFactory
from cart import ShoppingCartList, CartManager, AddItemCommand, RemoveItemCommand, UpdateQuantityCommand


def make_products():
    laptop = ProductFactory.create_product("Physical", "LPT-1", "Laptop", 1000.0, set(), 2.5)
    ebook = ProductFactory.create_product("Digital", "EBK-1", "Python Guide", 20.0, set())
    return laptop, ebook


class TestShoppingCartList(unittest.TestCase):
    def test_add_item_increases_subtotal(self):
        cart = ShoppingCartList()
        laptop, _ = make_products()
        cart.add(laptop, 1)
        self.assertEqual(cart.get_subtotal(), 1000.0)

    def test_add_same_sku_merges_quantity(self):
        cart = ShoppingCartList()
        laptop, _ = make_products()
        cart.add(laptop, 1)
        cart.add(laptop, 2)
        self.assertEqual(cart.get_item("LPT-1").quantity, 3)

    def test_remove_partial_quantity(self):
        cart = ShoppingCartList()
        laptop, _ = make_products()
        cart.add(laptop, 5)
        cart.remove("LPT-1", 2)
        self.assertEqual(cart.get_item("LPT-1").quantity, 3)

    def test_remove_all_deletes_node(self):
        cart = ShoppingCartList()
        laptop, _ = make_products()
        cart.add(laptop, 1)
        cart.remove("LPT-1")
        self.assertIsNone(cart.get_item("LPT-1"))

    def test_update_quantity(self):
        cart = ShoppingCartList()
        laptop, _ = make_products()
        cart.add(laptop, 1)
        cart.update_quantity("LPT-1", 10)
        self.assertEqual(cart.get_item("LPT-1").quantity, 10)


class TestCommandUndoRedo(unittest.TestCase):
    def test_undo_redo_add_item(self):
        cart = ShoppingCartList()
        manager = CartManager(cart)
        laptop, ebook = make_products()
        manager.execute_command(AddItemCommand(cart, laptop, 1))
        manager.execute_command(AddItemCommand(cart, ebook, 2))
        self.assertEqual(cart.get_subtotal(), 1040.0)

        manager.undo()
        self.assertEqual(cart.get_subtotal(), 1000.0)

        manager.redo()
        self.assertEqual(cart.get_subtotal(), 1040.0)

    def test_new_command_clears_redo_stack(self):
        cart = ShoppingCartList()
        manager = CartManager(cart)
        laptop, ebook = make_products()
        manager.execute_command(AddItemCommand(cart, laptop, 1))
        manager.undo()
        self.assertEqual(len(manager.redo_stack), 1)

        manager.execute_command(AddItemCommand(cart, ebook, 1))
        self.assertEqual(len(manager.redo_stack), 0)

    def test_undo_remove_item_restores_it(self):
        cart = ShoppingCartList()
        manager = CartManager(cart)
        laptop, _ = make_products()
        manager.execute_command(AddItemCommand(cart, laptop, 3))
        manager.execute_command(RemoveItemCommand(cart, "LPT-1", 1))
        self.assertEqual(cart.get_item("LPT-1").quantity, 2)

        manager.undo()
        self.assertEqual(cart.get_item("LPT-1").quantity, 3)

    def test_undo_update_quantity_restores_previous_value(self):
        cart = ShoppingCartList()
        manager = CartManager(cart)
        laptop, _ = make_products()
        manager.execute_command(AddItemCommand(cart, laptop, 1))
        manager.execute_command(UpdateQuantityCommand(cart, "LPT-1", 9))
        self.assertEqual(cart.get_item("LPT-1").quantity, 9)

        manager.undo()
        self.assertEqual(cart.get_item("LPT-1").quantity, 1)

    def test_undo_on_empty_stack_returns_false(self):
        cart = ShoppingCartList()
        manager = CartManager(cart)
        self.assertFalse(manager.undo())


if __name__ == "__main__":
    unittest.main()
