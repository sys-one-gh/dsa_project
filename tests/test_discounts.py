import unittest
from discounts import BaseOrder, FlatDiscount, PercentageDiscount, BuyOneGetOneFree


class TestDiscountDecorators(unittest.TestCase):
    def test_flat_discount(self):
        order = FlatDiscount(BaseOrder(100.0), 20.0)
        self.assertEqual(order.get_total(), 80.0)

    def test_flat_discount_does_not_go_negative(self):
        order = FlatDiscount(BaseOrder(10.0), 50.0)
        self.assertEqual(order.get_total(), 0.0)

    def test_percentage_discount(self):
        order = PercentageDiscount(BaseOrder(200.0), 0.10)
        self.assertAlmostEqual(order.get_total(), 180.0)

    def test_stacked_discounts_apply_in_order(self):
        order = PercentageDiscount(FlatDiscount(BaseOrder(1040.0), 50.0), 0.10)
        self.assertAlmostEqual(order.get_total(), 891.0)

    def test_bogo_removes_cheapest_item(self):
        order = BuyOneGetOneFree(BaseOrder(120.0), [100.0, 20.0])
        self.assertEqual(order.get_total(), 100.0)

    def test_bogo_no_effect_with_single_item(self):
        order = BuyOneGetOneFree(BaseOrder(100.0), [100.0])
        self.assertEqual(order.get_total(), 100.0)


if __name__ == "__main__":
    unittest.main()
