## Books Models
```mermaid
classDiagram
    direction LR
    class Category{
      +name: str
      +__str__()
    }
    class Publisher{
      +name: str
      +__str__()
    }
    class Author{
      +first_name: str
      +middle_name: str
      +last_name: str
      +full_name()
      +full_name_reversed()
      +__str__()
      +save()
    }
    class Book{
      +title: str
      +author: Author
      +publisher: Publisher
      +category: Category
      +format: tuple
      +description: str
      +published_at: Date
      +cover: ImageField
      +__str__()
      +is_published()
      +year_of_publication()
      +save()
    }
    Category "1" *-- "*" Book
    Publisher "1" *-- "*" Book
    Author "1" *-- "*" Book
```

## Related Signals

- **Book Created → Triggers BookInventory Creation**  
  When a new `Book` instance is created, a signal automatically creates a corresponding `BookInventory` entry.  
  (See [Signals Documentation](docs/signals.md) for details.)
