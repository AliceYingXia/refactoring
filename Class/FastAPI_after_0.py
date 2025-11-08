#%%
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
    base_price: Optional[float] = 0.0,
    age_discount: Optional[float] = 1.0,
    day_deduction: Optional[float] = 0.0,
):
    return math.ceil(base_price * age_discount * (1 - day_deduction/100) )


@app.get("/prices")
async def compute_price(
    type: str,
    age: Optional[int] = None,
    date: Optional[dt.date] = None,
):
    # Base price by type
    result = await database.fetch_one(
        select(base_price_table.c.cost).where(base_price_table.c.type == type)
    )

    # Free for kids under 6
    if age and age < 6:
        cost = compute_cost()
        return {"cost": cost}

    # Daytime pricing: apply reductions for Monday (non-holiday) and age bands
    if type != "night":
        # Teens (6–14) get 30% off of base cost (no Monday reduction mentioned in snippet)
        if age and age < 15:
            cost = compute_cost(result.cost, 0.7, 0)
            return {"cost": cost}

        holidays = await database.fetch_all(select(holidays_table))
        is_holiday = False
        reduction = 0

        # Check if selected date is a holiday
        for row in holidays:
            if date and date == row.holiday:
                is_holiday = True

        # Non-holiday Monday gets 35% reduction
        if not is_holiday and date and date.weekday() == 0:
            reduction = 35

        # No age provided: apply only the Monday/holiday reduction
        # Seniors (>64) get 25% off, and still apply Monday reduction if any
        if age and age > 64:
            cost = compute_cost(result.cost, 0.75, reduction)
            return {"cost": cost}
        else:
            # Everyone else: just the Monday reduction
            cost = compute_cost(result.cost, 1, reduction)
            return {"cost": cost}

    # Night pricing: different age handling per the snippet
    else:
        # Seniors (>64) pay 40% of base cost at night
        if age and age > 64:
            cost = compute_cost(result.cost, 0.4, 0)
            return {"cost": cost}
        else:
            # Others (>=6 and <=64): pay base cost
            cost = compute_cost(result.cost, 1, 0)
            return {"cost": cost}

