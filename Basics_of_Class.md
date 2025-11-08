# Basics of Class

## @dataclass and field
**automatically creates**

- \_\_init__(self, name, price, discount=0.0)

- \_\_repr__(self) (pretty print)

- \_\_eq__(self, other) (for comparisons)

```python
class Product:
    def __init__(self, name: str, price: float, discount: float = 0.0):
        self.name = name
        self.price = price
        self.discount = discount

    def __repr__(self):
        return f"Product(name={self.name!r}, price={self.price}, discount={self.discount})"
```

```python
from dataclasses import dataclass

@dataclass
class Product:
    name: str
    price: float
    discount: float = 0.0
```
**Use default_factory for all mutables**

- list → field(default_factory=list)

- dict → field(default_factory=dict)

- set → field(default_factory=set)

- Custom container → field(default_factory=MyContainer)

Use [] creates one shared list at class definition time, and every instance of the dataclass will reuse that same list. field(default_factory=list) creates a fresh list per instance, which is what you almost always want.

```python
from dataclasses import dataclass, field
import random

@dataclass
class Bucket:
    size: int = field(default_factory=lambda: random.randint(1, 10))
```

```python
from dataclasses import dataclass

@dataclass
class Order:
    items: list = []   # ❌ one shared list!

a = Order()
b = Order()
a.items.append("apple")
print(b.items)  # ['apple']  ← Oops: b sees a’s change
```

```python
from dataclasses import dataclass, field

@dataclass
class Order:
    items: list = field(default_factory=list)  # ✅ new list per instance

a = Order()
b = Order()
a.items.append("apple")
print(b.items)  # []  ← independent lists
```

## @classmethod is a decorator that makes a method receive the class as the first argument instead of the instance.

In other words:

Normal method: gets self (the object)

Class method: gets cls (the class itself)

- **Alternate constructor**

```python
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    @classmethod
    def from_string(cls, line):
        name, email = line.split(",")
        return cls(name.strip(), email.strip())
# usage
u = User.from_string("Alice, alice@gmail.com")
print(u.name, u.email)
```
- **Inheritance-friendly factory**
```python
class Shape:
    @classmethod
    def from_sides(cls, n):
        # returns an instance of the class it was called on
        return cls(n)

class Polygon(Shape):
    def __init__(self, sides):
        self.sides = sides

p = Polygon.from_sides(5)   # cls is Polygon → returns a Polygon
```
- **Class-level state**
```python
class Counter:
    count = 0

    @classmethod
    def bump(cls):
        cls.count += 1

Counter.bump(); Counter.bump()
print(Counter.count)  # 2
```

# [*, **, *args, **kwargs]
\* for tuple and \*\* for dictionary(key: val)
- **\* (bare asterisk)**

A separator that says: all parameters after this must be passed by keyword (keyword-only).
```python
def f(a, b, *, c, d=0):
    ...
# f(1, 2, 3, 4)        ❌ c and d must be named
# f(1, 2, c=3, d=4)    ✅
```
- **\*argsInheritance-friendly factory**

Collects any extra positional arguments into a tuple named args.
```python
def g(x, *args):
    print(args)  # tuple of extra positionals
g(1, 2, 3)  # args == (2, 3)
```
- **\*\*kwargs**

**kwargs and **extras both mean:

“collect any extra keyword arguments into a dictionary.”

So they behave identically.

Naming it **kwargs is just a convention — it stands for keyword arguments.

You can rename it to anything descriptive (like **extras, **options, or **params) if that better fits the context.
```python
def h(x, **kwargs):
    print(kwargs)  # dict of extra keywords
h(1, y=2, z=3)  # kwargs == {'y': 2, 'z': 3}
```
- **\*\*overrides**
```python
overrides = {"c": 10, "d": 20}
f(1, 2, **overrides)   # same as f(1, 2, c=10, d=20)
```
You can mix explicit keywords and an unpacked dict; if keys collide, later wins:
```python
f(1, 2, c=5, **{"c": 10, "d": 20})  # c becomes 10
```

- **\*iterable**
```python
params = (1, 2)
f(*params, c=3, d=4)
```

- **more examples**
```python
class Lead:
    def __init__(self, company_website, company_size, *, email=None, discount=1.0): ...

class Customer(Lead):
    def __init__(self, company_website, company_size, **kwargs):
        # caller can pass email=..., discount=..., loyalty=...
        self.loyalty = kwargs.pop("loyalty", 0)
        super().__init__(company_website, company_size, **kwargs)
```
```python
defaults = {"timeout": 3, "retries": 1}
client = HttpClient(**defaults, **{"timeout": 10})  # timeout overridden to 10
```
