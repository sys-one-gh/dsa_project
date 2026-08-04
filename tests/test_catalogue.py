import unittest
from models import ProductFactory
from catalogue import Catalogue


def make_catalogue():
    catalogue = Catalogue()
    catalogue.add_product(ProductFactory.create_product("Physical", "LPT-1", "Laptop", 1000.0, {"electronics", "sale"}, 2.5))
    catalogue.add_product(ProductFactory.create_product("Digital", "EBK-1", "Python Guide", 20.0, {"education", "digital"}))
    catalogue.add_product(ProductFactory.create_product("Subscription", "SUB-1", "Music Premium", 15.0, {"entertainment", "digital"}))
    return catalogue


class TestCatalogueCRUD(unittest.TestCase):
    def test_add_and_get_product(self):
        catalogue = make_catalogue()
        self.assertEqual(catalogue.get_product("LPT-1").name, "Laptop")

    def test_duplicate_sku_raises(self):
        catalogue = make_catalogue()
        with self.assertRaises(ValueError):
            catalogue.add_product(ProductFactory.create_product("Digital", "LPT-1", "Dup", 1.0, set()))

    def test_update_product_price_resorts_list(self):
        catalogue = make_catalogue()
        catalogue.update_product("SUB-1", price=5000.0)
        names_in_order = [p.name for p in catalogue.sorted_list.to_list()]
        self.assertEqual(names_in_order[-1], "Music Premium")

    def test_remove_product(self):
        catalogue = make_catalogue()
        catalogue.remove_product("EBK-1")
        self.assertIsNone(catalogue.get_product("EBK-1"))
        self.assertNotIn("Python Guide", [p.name for p in catalogue.sorted_list.to_list()])

    def test_remove_missing_product_raises(self):
        catalogue = make_catalogue()
        with self.assertRaises(KeyError):
            catalogue.remove_product("NOPE")


class TestCatalogueSearch(unittest.TestCase):
    def test_search_by_keyword(self):
        catalogue = make_catalogue()
        results = catalogue.search_by_keyword("guide")
        self.assertEqual([p.sku for p in results], ["EBK-1"])

    def test_search_by_tags_match_all(self):
        catalogue = make_catalogue()
        results = catalogue.search_by_tags({"digital"}, match_all=True)
        self.assertEqual({p.sku for p in results}, {"EBK-1", "SUB-1"})

    def test_search_by_tags_match_any(self):
        catalogue = make_catalogue()
        results = catalogue.search_by_tags({"sale", "entertainment"}, match_all=False)
        self.assertEqual({p.sku for p in results}, {"LPT-1", "SUB-1"})

    def test_sorted_list_ascending_order(self):
        catalogue = make_catalogue()
        prices = [p.price for p in catalogue.sorted_list.to_list()]
        self.assertEqual(prices, sorted(prices))


if __name__ == "__main__":
    unittest.main()
