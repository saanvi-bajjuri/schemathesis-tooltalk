"""Demo API for the Schemathesis tool talk.

Run:  uvicorn app:app --port 8000
Spec: http://127.0.0.1:8000/openapi.json   (docs at /docs)

FIXED VERSION: quantity must be >= 1, so the divide-by-zero cannot happen.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Shop API")

ITEMS = {
    1: {"name": "notebook", "price": 4.0},
    2: {"name": "pen", "price": 1.5},
}


class Order(BaseModel):
    item_id: int = Field(ge=1, le=2)
    quantity: int = Field(ge=1)  # FIXED


@app.get("/items/{item_id}", responses={404: {"description": "item not found"}})
def get_item(item_id: int):
    item = ITEMS.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="item not found")
    return item


@app.post(
    "/orders",
    responses={
        400: {"description": "malformed request body"},
        404: {"description": "item not found"},
    },
)
def create_order(order: Order):
    item = ITEMS.get(order.item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="item not found")
    shipping_per_item = 5.0 / order.quantity  # ZeroDivisionError when quantity == 0
    total = order.quantity * (item["price"] + shipping_per_item)
    return {"item": item["name"], "quantity": order.quantity, "total": round(total, 2)}