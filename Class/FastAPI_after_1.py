#%%
# after
# after
from typing import Optional
import datetime as dt
import math

from fastapi import FastAPI
from sqlalchemy import select

app = FastAPI()

# --- Assume these exist in your project ---
# async database client compatible with `fetch_one` / `fetch_all`
# and SQLAlchemy table objects with the shown columns.
database = ...  # e.g., databases.Database(...)
base_price_table = ...  # SQLAlchemy Table with columns: c.type, c.cost
holidays_table = ...    # SQLAlchemy Table with column: c.holiday
# -----------------------------------------

def compute_cost(
    basic_price: Optional[float] = 0.0,
    age_discount: Optional[float] = 1.0,
    day_deduction: Optional[float] = 0.0,
) -> int:
    return math.ceil(basic_price * age_discount * (1 - day_deduction) )

class BasicPrice:
    def __init__(self, price_type: str):
        self.price_type = price_type

    async def basic_cost(self) -> float:
        result = await database.fetch_one(
                select(base_price_table.c.cost).where(base_price_table.c.type == self.price_type)
                )
        if result is None or result.cost is None:
            raise ValueError(f'{self.price_type} does not have basic price!')
        return float(result.cost)

class Night(BasicPrice):

    def __init__(self,
                type: str,
                age: Optional[int] = None,
                date: Optional[dt.date] = None,):
        super().__init__(type)
        self.age = age
        self.date = date

    def get_discount(self) -> float:
        # Free for kids under 6
        if self.age and self.age < 6:
            return 0.0
        # Seniors (>64) pay 40% of base cost at night
        elif self.age and self.age > 64:
            return 0.4
        else:
            # Others (>=6 and <=64): pay base cost
            return 1.0

    def get_reduction(self) -> float:
        return 0.0

    async def cost(self) -> int:
        return compute_cost(await self.basic_cost(), self.get_discount(), self.get_reduction())


class Day(BasicPrice):
    # Daytime pricing: apply reductions for Monday (non-holiday) and age bands

    def __init__(self, price_type: str, age: Optional[int] = None, date: Optional[dt.date] = None):
        super().__init__(price_type)
        self.age = age
        self.date = date

    async def is_holiday(self) -> bool:
        holidays = await database.fetch_all(select(holidays_table))
        holidays = {row.holiday for row in holidays}
        return bool(self.date in holidays)


    def get_discount(self) -> float:
        # Free for kids under 6
        if self.age and self.age < 6:
            return 0.0
        # Seniors (>64) pay 40% of base cost at night
        elif self.age and self.age < 15:
            return 0.7
        elif self.age and self.age > 64:
            return 0.75
        else:
            # Others (>=6 and <=64): pay base cost
            return 1.0

    async def get_reduction(self) -> float:
        # Non-holiday Monday gets 35% reduction
        holiday_yes = await self.is_holiday()
        available_reduction = (self.age and self.age >= 15 and self.date and self.date.weekday() == 0 and not holiday_yes)
        if available_reduction:
            return 0.35
        else:
            return  0.0

    async def cost(self) -> int:
        return compute_cost(await self.basic_cost(), self.get_discount(), await self.get_reduction())

@app.get("/prices")
async def compute_price(
    type: str,
    age: Optional[int] = None,
    date: Optional[dt.date] = None,
):
    if type != "night":
        return {'cost' : await Day(type, age, date).cost() }
    else:
        return {'cost' : await Night(type, age, date).cost() }



