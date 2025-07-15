from sqlalchemy import Column, BigInteger, Numeric, String, DateTime, Text, ForeignKey
from app.database import Base

class Income(Base):
    __tablename__ = "income"

    id = Column(BigInteger, primary_key=True, index=True)
    id_user = Column(BigInteger, ForeignKey("user.id"))
    value = Column(Numeric)
    source = Column(String)
    received_at = Column(DateTime)
    description = Column(Text)
