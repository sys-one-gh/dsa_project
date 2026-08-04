import collections
from typing import List


class Order:
    """A submitted order."""

    _next_id = 1

    def __init__(self, items: List[str], final_total: float):
        self.order_id = Order._next_id
        Order._next_id += 1
        self.items: List[str] = items
        self.final_total = final_total
        self.status = "Pending"

    def mark_fulfilled(self):
        self.status = "Fulfilled"

    def __repr__(self):
        return f"Order#{self.order_id} [{self.status}] items={self.items} total=${self.final_total:.2f}"


class OrderProcessor:
    """FIFO order queue for the fulfilment module."""

    def __init__(self):
        self.order_queue: collections.deque = collections.deque()
        self.order_history: List[Order] = []

    def submit_order(self, order: Order):
        self.order_queue.append(order)
        print(f"Order #{order.order_id} added to queue.")

    def process_orders(self):
        while self.order_queue:
            order = self.order_queue.popleft()
            order.mark_fulfilled()
            self.order_history.append(order)
            print(f"Processing {order}")
