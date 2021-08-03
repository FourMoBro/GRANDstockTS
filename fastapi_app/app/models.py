from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from pgdb_config import Base


class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    symbol = Column(String)
    figi = Column(String)
    type = Column(String)
    url = Column(String)

    