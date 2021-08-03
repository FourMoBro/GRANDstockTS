from typing import List
from fastapi import FastAPI, Request, Depends, HTTPException
from sqlalchemy.orm import Session

from fastapi.templating import Jinja2Templates

import models, pgdb_crud, pgdb_schema
from pgdb_config import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Stock SCreener API"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

templates = Jinja2Templates(directory="templates")

@app.get("/")
def dashboard(request: Request):
    """
    This displays the main dashboard for the app.
    """
    context = {
        "request": request
        }
    return templates.TemplateResponse("dashboard.html", context)

@app.post("/stocks/", response_model=pgdb_schema.Stock)
def create_stock(stock: pgdb_schema.StockCreate, db: Session = Depends(get_db)):
    """
    This is where you can create a stock.
    """
    db_stock = pgdb_crud.get_stock_by_symbol(db, symbol=stock.symbol)
    if db_stock:
        raise HTTPException(status_code=400, detail="Symbol already exists")
    return pgdb_crud.create_stock(db=db, stock=stock)

@app.get("/stocks/", response_model=List[pgdb_schema.Stock])
def read_stocks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    stocks = pgdb_crud.get_stocks(db, skip=skip, limit=limit)
    return stocks

@app.get("/stocks/{stock_id}", response_model=pgdb_schema.Stock)
def read_stock(stock_id: str, db: Session = Depends(get_db)):
    db_stock = pgdb_crud.get_stock_by_symbol(db, symbol=stock_id)
    if db_stock is None:
        raise HTTPException(status_code=404, detail="stock not found")
    return db_stock
    