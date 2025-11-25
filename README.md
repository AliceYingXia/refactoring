# Refactoring Examples

A comprehensive educational repository demonstrating refactoring techniques and best practices in Python, from basic concepts to production-ready code patterns.

## Table of Contents

- [About](#about)
- [What is Refactoring?](#what-is-refactoring)
- [Repository Structure](#repository-structure)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Learning Path](#learning-path)
- [Examples Covered](#examples-covered)
- [Key Refactoring Techniques](#key-refactoring-techniques)
- [Technologies Used](#technologies-used)

## About

This repository provides hands-on examples of code refactoring in Python, demonstrating how to transform poorly written code into clean, maintainable, and production-ready solutions. Each example shows a clear progression from "before" to "after" states, making it easy to understand the benefits of each refactoring technique.

## What is Refactoring?

Refactoring is the process of restructuring existing code without changing its external behavior. The goal is to improve code quality, readability, maintainability, and performance while preserving functionality.

## Repository Structure

```
refactoring/
├── Basics_of_Class.md              # Guide to @dataclass, @classmethod, *args/**kwargs
├── Basics_of_Decorator.md          # Python decorators explained
├── Get_Your_Hands_Dirty.ipynb      # Interactive exercises
├── PEP8_Exercise.ipynb             # PEP8 standards and advanced patterns
├── class/                          # Core refactoring examples
│   ├── crm_before.py               # CRM app with anti-patterns
│   ├── crm_after_0.py              # First refactoring (extract functions)
│   ├── crm_after_1.py              # Adding type hints
│   ├── crm_after_2.py              # Using @dataclass
│   ├── crm_after_3.py              # Final version with @classmethod
│   ├── FastAPI_before.py           # Complex nested conditionals
│   ├── FastAPI_after_0.py          # Extracted helper functions
│   └── FastAPI_after_1.py          # OOP design with inheritance
└── Mistral_chat_service_FastAP/    # Production-ready FastAPI + LLM service
    ├── main_before.py              # Basic API endpoint
    ├── main_after_0.py             # Production-ready version
    ├── mistral_helper_before.py    # Simple client wrapper
    └── mistral_helper_after_0.py   # Robust error handling
```

## Prerequisites

- Python 3.8+
- Basic understanding of Python syntax
- Familiarity with object-oriented programming concepts (helpful but not required)

### Optional Dependencies

For running specific examples, you may need:
```bash
pip install fastapi uvicorn pydantic mistralai sqlalchemy pandas jupyter
```

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd refactoring
   ```

2. **Start with the educational materials:**
   - Read `Basics_of_Class.md` to understand Python dataclasses and class methods
   - Read `Basics_of_Decorator.md` to learn about decorators

3. **Try the interactive exercises:**
   ```bash
   jupyter notebook Get_Your_Hands_Dirty.ipynb
   ```

4. **Study the progressive examples:**
   - Compare `class/crm_before.py` with its refactored versions (`crm_after_0.py` through `crm_after_3.py`)
   - See how each iteration improves the code

## Learning Path

### Beginner Level
1. Start with `Basics_of_Class.md` and `Basics_of_Decorator.md`
2. Work through `Get_Your_Hands_Dirty.ipynb`
3. Study the CRM example progression (`class/crm_*.py`)

### Intermediate Level
1. Review `PEP8_Exercise.ipynb` for style conventions
2. Examine the FastAPI pricing examples (`class/FastAPI_*.py`)
3. Learn about extracting functions and DRY principle

### Advanced Level
1. Study the Mistral chat service examples (`Mistral_chat_service_FastAP/`)
2. Focus on async/await patterns, error handling, and production-ready code
3. Understand custom exception classes and proper API design

## Examples Covered

### 1. CRM Application Refactoring (`class/crm_*.py`)
Progressive refactoring of a customer relationship management application:
- **Before:** Monolithic code with poor structure
- **After 0:** Extracted functions for better organization
- **After 1:** Added type hints for clarity
- **After 2:** Implemented `@dataclass` for cleaner code
- **After 3:** Used `@classmethod` for factory patterns

**Key lessons:** Function extraction, type hints, dataclasses, class methods, avoiding mutable defaults

### 2. FastAPI Price Computation (`class/FastAPI_*.py`)
Refactoring complex pricing logic in a FastAPI application:
- **Before:** Nested conditionals and repeated logic
- **After 0:** Extracted `compute_cost()` helper function
- **After 1:** Object-oriented design with inheritance

**Key lessons:** DRY principle, extracting pure functions, OOP design patterns

### 3. Mistral Chat Service (`Mistral_chat_service_FastAP/`)
Building a production-ready FastAPI service with LLM integration:
- **Before:** Basic implementation without error handling
- **After:** Robust service with validation, error handling, and health checks

**Key lessons:** Custom exceptions, async patterns, request validation, environment variables, docstrings

## Key Refactoring Techniques

This repository demonstrates the following refactoring techniques:

1. **Function Extraction** - Breaking down long functions into smaller, focused ones
2. **Type Hints** - Adding Python type annotations for clarity and IDE support
3. **Dataclasses** - Using `@dataclass` decorator instead of boilerplate code
4. **Factory Methods** - Using `@classmethod` for flexible object creation
5. **Error Handling** - Custom exception classes with proper context
6. **Async/Await** - Proper asynchronous programming patterns
7. **DRY Principle** - Eliminating code duplication through abstraction
8. **PEP8 Compliance** - Following Python style guidelines
9. **Separation of Concerns** - Dividing business logic from infrastructure code
10. **Documentation** - Writing clear docstrings and comments

## Technologies Used

- **FastAPI** - Modern web framework for building APIs
- **Pydantic** - Data validation using Python type annotations
- **Mistral AI SDK** - Integration with Mistral LLM services
- **SQLAlchemy** - SQL toolkit and ORM
- **Pandas** - Data manipulation and analysis
- **Jupyter** - Interactive notebooks for learning

---

**Happy Refactoring!** Feel free to explore the examples, experiment with the code, and apply these techniques to your own projects. 
