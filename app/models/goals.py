from sqlalchemy import Column, BigInteger, Integer, Numeric, Date, ForeignKey
from app.database import Base

class Goals(Base):
    __tablename__ = "goals"

    id = Column(BigInteger, primary_key=True, index=True)
    id_user = Column(BigInteger, ForeignKey("user.id"))
    id_category = Column(Integer, ForeignKey("category.id"))
    target_value = Column(Numeric)
    period_start = Column(Date)
    period_end = Column(Date)
