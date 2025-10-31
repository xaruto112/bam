from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Watermelon
import json

class DatabaseManager:
    def __init__(self, db_url="sqlite:///watermelons.db"):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        
    def create_database(self):
        """Создает базу данных и таблицы"""
        Base.metadata.create_all(self.engine)
        print("База данных создана успешно!")
        
    def init_sample_data(self):
        """Добавляет примеры арбузов в базу данных"""
        session = self.Session()
        
        # Проверяем, есть ли уже данные
        if session.query(Watermelon).count() == 0:
            sample_watermelons = [
                Watermelon(
                    variety="Кримсон Свит",
                    weight=4.5,
                    sweetness=8,
                    ripeness="спелый",
                    price=45.0,
                    is_organic=True,
                    supplier="Ферма 'Солнечная'"
                ),
                Watermelon(
                    variety="Астраханский",
                    weight=6.2,
                    sweetness=9,
                    ripeness="очень спелый",
                    price=50.0,
                    is_organic=False,
                    supplier="Астраханские поля"
                ),
                Watermelon(
                    variety="Шуга Бейби",
                    weight=3.8,
                    sweetness=7,
                    ripeness="спелый",
                    price=55.0,
                    is_organic=True,
                    supplier="Органическая ферма"
                ),
                Watermelon(
                    variety="Чарльстон Грей",
                    weight=5.5,
                    sweetness=6,
                    ripeness="средней спелости",
                    price=40.0,
                    is_organic=False,
                    supplier="Импортные фрукты"
                ),
                Watermelon(
                    variety="Холодок",
                    weight=7.1,
                    sweetness=8,
                    ripeness="спелый",
                    price=48.0,
                    is_organic=True,
                    supplier="Сибирские бахчи"
                )
            ]
            
            session.add_all(sample_watermelons)
            session.commit()
            print("Добавлены примеры арбузов в базу данных!")
        else:
            print("В базе данных уже есть данные.")
            
        session.close()