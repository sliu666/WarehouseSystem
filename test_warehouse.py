import unittest

from warehouse import Warehouse


class WarehouseTests(unittest.TestCase):
    def setUp(self):
        self.warehouse = Warehouse()
        self.warehouse.receive(10)

    def test_receive_and_ship(self):
        self.warehouse.ship(3)
        self.assertEqual(self.warehouse.stock, 7)

    def test_ship_all_stock(self):
        self.warehouse.ship(10)
        self.assertEqual(self.warehouse.stock, 0)

    def test_cannot_ship_more_than_stock(self):
        with self.assertRaises(ValueError):
            self.warehouse.ship(11)
        self.assertEqual(self.warehouse.stock, 10)

    def test_quantities_must_be_positive(self):
        for operation in (self.warehouse.receive, self.warehouse.ship):
            for quantity in (0, -1):
                with self.subTest(operation=operation.__name__, quantity=quantity):
                    with self.assertRaises(ValueError):
                        operation(quantity)
        self.assertEqual(self.warehouse.stock, 10)


if __name__ == "__main__":
    unittest.main()