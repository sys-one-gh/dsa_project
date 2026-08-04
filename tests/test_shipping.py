import unittest
from models import ProductFactory
from cart import ShoppingCartList
from shipping import ShippingFacade


class TestShippingFacade(unittest.TestCase):
    def test_domestic_shipping_cost(self):
        cart = ShoppingCartList()
        laptop = ProductFactory.create_product("Physical", "LPT-1", "Laptop", 1000.0, set(), 2.5)
        cart.add(laptop, 1)
        cost = ShippingFacade.calculate_shipping(cart, "Domestic")
        self.assertAlmostEqual(cost, 10.0)

    def test_international_shipping_costs_more(self):
        cart = ShoppingCartList()
        laptop = ProductFactory.create_product("Physical", "LPT-1", "Laptop", 1000.0, set(), 2.5)
        cart.add(laptop, 1)
        domestic = ShippingFacade.calculate_shipping(cart, "Domestic")
        international = ShippingFacade.calculate_shipping(cart, "International")
        self.assertGreater(international, domestic)

    def test_digital_products_add_no_weight(self):
        cart = ShoppingCartList()
        ebook = ProductFactory.create_product("Digital", "EBK-1", "Python Guide", 20.0, set())
        cart.add(ebook, 5)
        cost = ShippingFacade.calculate_shipping(cart, "Domestic")
        self.assertEqual(cost, 5.0)  # base rate only, zero weight


if __name__ == "__main__":
    unittest.main()
