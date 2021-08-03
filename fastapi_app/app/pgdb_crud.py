from sqlalchemy.orm import Session

import models, pgdb_schema

def get_stock_by_symbol(db: Session, symbol: str):
    return db.query(models.Stock).filter(models.Stock.symbol == symbol).first()

def get_stocks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Stock).offset(skip).limit(limit).all()

def create_stock(db: Session, stock: pgdb_schema.StockCreate):
    
    db_stock = models.Stock(symbol=stock.symbol)
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock