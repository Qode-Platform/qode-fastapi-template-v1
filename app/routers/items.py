"""One router per resource; main.py only wires them together."""

from fastapi import APIRouter, HTTPException

from app.models import Item, ItemIn

router = APIRouter(prefix="/items", tags=["items"])

_ITEMS: dict[int, Item] = {}
_NEXT_ID = iter(range(1, 1_000_000))


@router.get("")
async def list_items() -> list[Item]:
    return list(_ITEMS.values())


@router.post("", status_code=201)
async def create_item(payload: ItemIn) -> Item:
    item = Item(id=next(_NEXT_ID), **payload.model_dump())
    _ITEMS[item.id] = item
    return item


@router.get("/{item_id}")
async def get_item(item_id: int) -> Item:
    if item_id not in _ITEMS:
        raise HTTPException(status_code=404, detail="item not found")
    return _ITEMS[item_id]
