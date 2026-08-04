import unittest
from models import ProductFactory, PhysicalProduct, DigitalProduct, SubscriptionProduct


class TestProductFactory(unittest.TestCase):
    def test_creates_physical_product(self):
        p = ProductFactory.create_product("Physical", "SKU1", "Chair", 50.0, {"furniture"}, 5.0)
        self.assertIsInstance(p, PhysicalProduct)
        self.assertEqual(p.weight, 5.0)

    def test_creates_digital_product(self):
        p = ProductFactory.create_product("Digital", "SKU2", "E-book", 10.0, {"books"})
        self.assertIsInstance(p, DigitalProduct)

    def test_creates_subscription_product(self):
        p = ProductFactory.create_product("Subscription", "SKU3", "Plan", 15.0, {"service"})
        self.assertIsInstance(p, SubscriptionProduct)

    def test_invalid_type_raises(self):
        with self.assertRaises(ValueError):
            ProductFactory.create_product("Bogus", "SKU4", "X", 1.0, set())

    def test_physical_product_tax(self):
        p = ProductFactory.create_product("Physical", "SKU1", "Chair", 100.0, set(), 5.0)
        self.assertAlmostEqual(p.calculate_tax(), 13.0)

    def test_digital_product_tax(self):
        p = ProductFactory.create_product("Digital", "SKU2", "E-book", 100.0, set())
        self.assertAlmostEqual(p.calculate_tax(), 5.0)

    def test_subscription_product_tax_is_zero(self):
        p = ProductFactory.create_product("Subscription", "SKU3", "Plan", 100.0, set())
        self.assertEqual(p.calculate_tax(), 0.0)

    def test_digital_product_weight_is_zero(self):
        p = ProductFactory.create_product("Digital", "SKU2", "E-book", 10.0, set())
        self.assertEqual(p.get_weight(), 0.0)


if __name__ == "__main__":
    unittest.main()
