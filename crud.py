from sqlalchemy import or_, and_
from models import Watermelon
from database import DatabaseManager

class WatermelonCRUD:
    def __init__(self):
        self.db = DatabaseManager()
        self.session = self.db.Session()
        
    def add_watermelon(self, variety, weight, sweetness, ripeness, price, is_organic=False, supplier=""):
        """Добавляет новый арбуз в базу данных"""
        watermelon = Watermelon(
            variety=variety,
            weight=weight,
            sweetness=sweetness,
            ripeness=ripeness,
            price=price,
            is_organic=is_organic,
            supplier=supplier
        )
        
        self.session.add(watermelon)
        self.session.commit()
        print(f"Арбуз сорта '{variety}' добавлен в базу данных!")
        return watermelon
    
    def get_all_watermelons(self):
        """Возвращает все арбузы"""
        return self.session.query(Watermelon).all()
    
    def find_by_sweetness(self, min_sweetness=7):
        """Находит арбузы с минимальной сладостью"""
        return self.session.query(Watermelon).filter(
            Watermelon.sweetness >= min_sweetness
        ).all()
    
    def find_by_weight_range(self, min_weight, max_weight):
        """Находит арбузы в диапазоне веса"""
        return self.session.query(Watermelon).filter(
            and_(
                Watermelon.weight >= min_weight,
                Watermelon.weight <= max_weight
            )
        ).all()
    
    def find_organic(self):
        """Находит органические арбузы"""
        return self.session.query(Watermelon).filter(
            Watermelon.is_organic == True
        ).all()
    
    def find_by_variety(self, variety):
        """Находит арбузы по сорту"""
        return self.session.query(Watermelon).filter(
            Watermelon.variety.ilike(f"%{variety}%")
        ).all()
    
    def get_best_quality(self, limit=5):
        """Возвращает арбузы с наивысшей оценкой качества"""
        watermelons = self.get_all_watermelons()
        sorted_watermelons = sorted(watermelons, key=lambda x: x.quality_score(), reverse=True)
        return sorted_watermelons[:limit]
    
    def get_cheapest_options(self, max_price_per_kg):
        """Находит самые дешевые варианты"""
        return self.session.query(Watermelon).filter(
            Watermelon.price <= max_price_per_kg
        ).order_by(Watermelon.price).all()
    
    def update_watermelon(self, watermelon_id, **kwargs):
        """Обновляет данные арбуза"""
        watermelon = self.session.query(Watermelon).filter(Watermelon.id == watermelon_id).first()
        if watermelon:
            for key, value in kwargs.items():
                setattr(watermelon, key, value)
            self.session.commit()
            print(f"Арбуз ID {watermelon_id} обновлен!")
        return watermelon
    
    def delete_watermelon(self, watermelon_id):
        """Удаляет арбуз из базы данных"""
        watermelon = self.session.query(Watermelon).filter(Watermelon.id == watermelon_id).first()
        if watermelon:
            self.session.delete(watermelon)
            self.session.commit()
            print(f"Арбуз ID {watermelon_id} удален!")
            return True
        return False
    
    def close(self):
        """Закрывает сессию"""
        self.session.close()