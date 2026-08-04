import unittest
from orders import Order, OrderProcessor


class TestOrderProcessorQueue(unittest.TestCase):
    def test_orders_processed_in_fifo_order(self):
        processor = OrderProcessor()
        first = Order(["A"], 10.0)
        second = Order(["B"], 20.0)
        processor.submit_order(first)
        processor.submit_order(second)

        processor.process_orders()

        self.assertEqual(processor.order_history, [first, second])

    def test_process_orders_marks_fulfilled(self):
        processor = OrderProcessor()
        order = Order(["A"], 10.0)
        processor.submit_order(order)
        processor.process_orders()
        self.assertEqual(order.status, "Fulfilled")

    def test_queue_empty_after_processing(self):
        processor = OrderProcessor()
        processor.submit_order(Order(["A"], 10.0))
        processor.process_orders()
        self.assertEqual(len(processor.order_queue), 0)


if __name__ == "__main__":
    unittest.main()
