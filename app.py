from fastapi import FastAPI, HTTPException
from fastapi.concurrency import run_in_threadpool

from utils.mysql_utils import init_db
import utils.mysql_utils as db


app = FastAPI(
    title="InventoryTrack API",
    description="A simple REST API for managing products and inventory stock.",
    version="1.0.0",
)


init_db()


@app.get("/")
async def root():
    return {
        "message": "InventoryTrack API is running",
        "version": "1.0.0",
        "docs": "/docs",
    }


# -------------------------
# Product Management
# -------------------------

@app.post("/products", tags=["Products"])
async def create_product(payload: dict):
    try:
        return await run_in_threadpool(db.create_product, payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/products", tags=["Products"])
async def get_products(
    limit: int = 10,
    offset: int = 0,
    search: str = None,
):
    return await run_in_threadpool(
        db.get_products,
        limit,
        offset,
        search,
    )


@app.get("/products/{pid}", tags=["Products"])
async def get_product(pid: int):
    data = await run_in_threadpool(db.get_product, pid)

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return data


@app.put("/products/{pid}", tags=["Products"])
async def update_product(pid: int, payload: dict):
    try:
        return await run_in_threadpool(
            db.update_product,
            pid,
            payload,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/products/{pid}", tags=["Products"])
async def delete_product(pid: int):
    return await run_in_threadpool(
        db.delete_product,
        pid,
    )


# -------------------------
# Inventory Management
# -------------------------

@app.post("/inventory/add", tags=["Inventory"])
async def add_stock(payload: dict):
    try:
        return await run_in_threadpool(
            db.add_stock,
            payload,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/inventory/remove", tags=["Inventory"])
async def remove_stock(payload: dict):
    try:
        return await run_in_threadpool(
            db.remove_stock,
            payload,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))