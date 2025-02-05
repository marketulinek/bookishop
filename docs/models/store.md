## Store App
```mermaid
classDiagram
    direction LR
    class Book
    note for Book "Defined in the Book App"
    class BookInventory{
        +book: Book
        +quantity_in_hand: int
        +min_stock_limit: int
        +max_stock_limit: int
        +reorder_point: int
        +__str__()
        +quantity_available()
        +for_sale()
        +in_stock()
        +inventory_status_code()
        +inventory_status()
        +in_stock_admin()
        +pre_order()
    }
    Book "1" *-- "1" BookInventory
```

## Related Signals

- **Created by Signal**  
  `BookInventory` instances are automatically created when a new `Book` is added.  
  (See [Signals Documentation](../signals.md) for details.)
