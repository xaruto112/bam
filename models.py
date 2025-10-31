from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Watermelon(Base):
    __tablename__ = 'watermelons'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    variety = Column(String(100), nullable=False)  # сорт
    weight = Column(Float, nullable=False)  # вес в кг
    sweetness = Column(Integer, nullable=False)  # сладость (1-10)
    ripeness = Column(String(50), nullable=False)  # спелость
    price = Column(Float, nullable=False)  # цена за кг
    is_organic = Column(Boolean, default=False)
    supplier = Column(String(100))
    created_date = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<Watermelon(variety='{self.variety}', weight={self.weight}kg, sweetness={self.sweetness}, price={self.price} руб/кг)>"
    
    def total_price(self):
        return self.weight * self.price
    
    def quality_score(self):
        """Рассчитывает оценку качества арбуза"""
        base_score = self.sweetness * 2
        if self.is_organic:
            base_score += 5
        if self.weight > 5:
            base_score += 3
        elif self.weight > 3:
            base_score += 1
        return base_score
    