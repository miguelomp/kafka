from fastapi import FastAPI

from .routers import orders

app = FastAPI()
app.include_router(orders.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

