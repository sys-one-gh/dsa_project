# Project 2: E-Commerce Inventory & Order Processing Engine

## MVP & Goals

**What we're trying to achieve:** demonstrate correct, working use of six core data structures and four GoF design patterns inside one coherent system, not six/four disconnected demos. The e-commerce domain (catalogue → cart → checkout → fulfilment) exists to give each structure and pattern a natural, meaningful reason to be there, so the implementation reads as real backend code rather than a textbook exercise.

**MVP — the minimum the project must do to satisfy the brief:**
- A product catalogue with full CRUD (Create/Read/Update/Delete) plus keyword and tag search.
- A shopping cart a user can add to, remove from, and update quantities in.
- Undo/redo on every cart edit.
- A checkout flow that stacks discounts and computes shipping.
- An order queue that processes submitted orders in FIFO order.
- A console entry point (`main.py`) a user can actually run and interact with, so every feature above is reachable and screenshot-able.
- A test suite covering each module (≥10 cases, per the marking scheme).

Everything beyond that MVP (UML diagram, technical report, git/task-board evidence, oral presentation) is grading scaffolding layered on top — the code itself only needs to satisfy the bullets above to be functionally complete.

## 2.1 Project Overview
Build a console-based e-commerce back-end engine (any tool/language) that manages product inventory, shopping carts, order processing, discount computation, and shipping-cost estimation. The system must make meaningful use of lists, stacks, queues, dictionaries, sorted linked lists, and sets, while demonstrating at least four GoF design patterns.

## 2.2 Learning Objectives
- Use generic collections (`List<T>`, `Dictionary<TKey, TValue>`, `HashSet<T>`, `Queue<T>`, `Stack<T>`) and custom linked / sorted linked lists.
- Apply the Factory Method, Decorator, Command, and Facade design patterns.
- Reason about trade-offs between data structures for different operations.
- Produce clean, testable code following SOLID principles.
- Document architecture decisions in a technical report.

## 2.3 Functional Requirements
- **Product Catalogue:** Store products in a `Dictionary<string, Product>` keyed by SKU. Support CRUD operations and keyword search.
- **Category Tags:** Each product has a `HashSet<string>` of tags (e.g., "electronics", "sale"). Use set operations (union, intersection) to power multi-tag filtering.
- **Shopping Cart:** Implement as a custom linked list of `CartItem` nodes. Support add, remove, update quantity, and calculate subtotal by traversing the list.
- **Order Queue:** Submitted orders enter a `Queue<Order>` for FIFO processing by the fulfilment module.
- **Undo / Redo for Cart:** Use two Stacks (undo stack, redo stack) of Command objects to allow customers to undo and redo cart modifications.
- **Price Sorted Display:** Maintain a sorted linked list of products by price for "browse by price" functionality.
- **Discount Decorator:** Wrap an `IOrder` object with one or more discount decorators — `PercentageDiscount`, `FlatDiscount`, `BuyOneGetOneFree` — that modify the total at each layer.
- **Shipping Calculator Facade:** A `ShippingFacade` hides the complexity of weight calculation, zone lookup, and carrier API stubs, exposing a single `CalculateShipping(order)` method.
- **Product Factory:** Use Factory Method to create product objects — `PhysicalProduct`, `DigitalProduct`, `SubscriptionProduct` — each with different shipping and tax logic.

## 2.4 Design Patterns Required
| Pattern | Where Applied | Purpose |
|---|---|---|
| Factory Method | `ProductFactory` | Instantiate correct Product subtype from input. |
| Decorator | `IOrder` / `DiscountDecorator` | Layer multiple discounts onto an order dynamically. |
| Command | `ICartCommand` (AddItem, RemoveItem, UpdateQty) | Enable undo / redo for shopping-cart edits. |
| Facade | `ShippingFacade` | Simplify the shipping-cost calculation subsystem. |

## 2.5 Marking Scheme (Total: 100 marks)
| Assessment Criteria | Weight (%) | Max Marks |
|---|---|---|
| Correct implementation of six data structures | 25 | 25 |
| Correct implementation of four design patterns | 25 | 25 |
| Code quality (SOLID, naming, modularity) | 10 | 10 |
| Unit / integration tests (minimum 10 test cases) | 10 | 10 |
| UML class diagram and technical report | 10 | 10 |
| Git commit history and task-board evidence | 10 | 10 |
| Oral presentation and individual Q&A | 10 | 10 |
| **Total** | **100** | **100** |
