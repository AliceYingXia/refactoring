# before
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
        return {"cost": 0}

    # Daytime pricing: apply reductions for Monday (non-holiday) and age bands
    if type != "night":
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

        # Teens (6–14) get 30% off of base cost (no Monday reduction mentioned in snippet)
        if age and age < 15:
            return {"cost": math.ceil(result.cost * 0.7)}
        else:
            # No age provided: apply only the Monday/holiday reduction
            if not age:
                cost = result.cost * (1 - reduction / 100)
                return {"cost": math.ceil(cost)}
            else:
                # Seniors (>64) get 25% off, and still apply Monday reduction if any
                if age > 64:
                    cost = result.cost * 0.75 * (1 - reduction / 100)
                    return {"cost": math.ceil(cost)}
                # Everyone else: just the Monday reduction
                cost = result.cost * (1 - reduction / 100)
                return {"cost": math.ceil(cost)}

    # Night pricing: different age handling per the snippet
    else:
        if age and age >= 6:
            # Seniors (>64) pay 40% of base cost at night
            if age > 64:
                return {"cost": math.ceil(result.cost * 0.4)}
            # Others (>=6 and <=64): pay base cost
            return result
        # Under 6: free
        return {"cost": 0}
