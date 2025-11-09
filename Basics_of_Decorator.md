# Basics of Decorators

**A decorator is Python is just a function that takes another function (or method, or class) as input, adds some extra behaviros, and returns a new function.**

**Syntactically, it is the thing with the @ sign you put above a function definition.**

```python
def greet():
    print('Hello')
# now you want to add some extra behavior before and after greet() runs, without changing its code.
# you can write a wrapper function
def my_decorator(func):
    def wrapper():
        print("Before the function runs")
        func() # call the original function
        print('After the function runs')
    return wrapper
# manually
decorated_greet = my_decorator(greet)
decorated_greet
# Before the function runs
# Hello!
# After the function runs
# using @
@my_decorator
def greet():
    print('Hello!')
```
**Decorator with arguments (*args, **kwargs)**
```python
def my_decorator(func):
    def wrapper(*args, *kwargs):
        print('Before')
        result = func(*args, *kwargs)
        print('After')
        return result
    return wrapper

@my_decorator
def add(a, b):
    print("Adding...")
    return a + b

res = add(2, 3)
print("Result:", res)
# Before
# Adding...
# After
# Result: 5
```
