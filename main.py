from database import DatabaseManager
from crud import WatermelonCRUD
import sys

def print_watermelon_info(watermelon):
    """Выводит информацию об арбузе в красивом формате"""
    print(f"\n{'='*50}")
    print(f"🍉 АРБУЗ #{watermelon.id}")
    print(f"{'='*50}")
    print(f"Сорт: {watermelon.variety}")
    print(f"Вес: {watermelon.weight} кг")
    print(f"Сладость: {watermelon.sweetness}/10")
    print(f"Спелость: {watermelon.ripeness}")
    print(f"Цена: {watermelon.price} руб/кг")
    print(f"Общая стоимость: {watermelon.total_price():.2f} руб")
    print(f"Органический: {'Да' if watermelon.is_organic else 'Нет'}")
    print(f"Поставщик: {watermelon.supplier}")
    print(f"Оценка качества: {watermelon.quality_score()}/25")
    print(f"{'='*50}")

def main():
    # Инициализация базы данных
    db = DatabaseManager()
    db.create_database()
    db.init_sample_data()
    
    crud = WatermelonCRUD()
    
    while True:
        print("\n" + "="*60)
        print("🎯 СИСТЕМА ВЫБОРА АРБУЗОВ")
        print("="*60)
        print("1. Показать все арбузы")
        print("2. Найти сладкие арбузы (сладость ≥ 7)")
        print("3. Найти по весу")
        print("4. Показать органические арбузы")
        print("5. Найти по сорту")
        print("6. Лучшие по качеству")
        print("7. Бюджетные варианты")
        print("8. Добавить новый арбуз")
        print("9. Обновить арбуз")
        print("10. Удалить арбуз")
        print("0. Выход")
        print("="*60)
        
        choice = input("Выберите действие: ").strip()
        
        if choice == "1":
            print("\n📋 ВСЕ АРБУЗЫ:")
            watermelons = crud.get_all_watermelons()
            for wm in watermelons:
                print_watermelon_info(wm)
                
        elif choice == "2":
            print("\n🍬 СЛАДКИЕ АРБУЗЫ:")
            watermelons = crud.find_by_sweetness(7)
            for wm in watermelons:
                print_watermelon_info(wm)
                
        elif choice == "3":
            try:
                min_w = float(input("Минимальный вес (кг): "))
                max_w = float(input("Максимальный вес (кг): "))
                watermelons = crud.find_by_weight_range(min_w, max_w)
                print(f"\n⚖️ АРБУЗЫ ВЕСОМ ОТ {min_w} ДО {max_w} КГ:")
                for wm in watermelons:
                    print_watermelon_info(wm)
            except ValueError:
                print("❌ Ошибка: введите корректные числа!")
                
        elif choice == "4":
            print("\n🌱 ОРГАНИЧЕСКИЕ АРБУЗЫ:")
            watermelons = crud.find_organic()
            for wm in watermelons:
                print_watermelon_info(wm)
                
        elif choice == "5":
            variety = input("Введите название сорта: ").strip()
            watermelons = crud.find_by_variety(variety)
            print(f"\n🔍 РЕЗУЛЬТАТЫ ПОИСКА ПО СОРТУ '{variety}':")
            for wm in watermelons:
                print_watermelon_info(wm)
                
        elif choice == "6":
            print("\n🏆 ЛУЧШИЕ ПО КАЧЕСТВУ:")
            watermelons = crud.get_best_quality()
            for i, wm in enumerate(watermelons, 1):
                print(f"\n🏅 МЕСТО #{i}:")
                print_watermelon_info(wm)
                
        elif choice == "7":
            try:
                max_price = float(input("Максимальная цена за кг: "))
                watermelons = crud.get_cheapest_options(max_price)
                print(f"\n💰 БЮДЖЕТНЫЕ ВАРИАНТЫ (до {max_price} руб/кг):")
                for wm in watermelons:
                    print_watermelon_info(wm)
            except ValueError:
                print("❌ Ошибка: введите корректную цену!")
                
        elif choice == "8":
            print("\n➕ ДОБАВЛЕНИЕ НОВОГО АРБУЗА:")
            try:
                variety = input("Сорт: ")
                weight = float(input("Вес (кг): "))
                sweetness = int(input("Сладость (1-10): "))
                ripeness = input("Спелость: ")
                price = float(input("Цена за кг: "))
                organic = input("Органический (да/нет): ").lower() == "да"
                supplier = input("Поставщик: ")
                
                crud.add_watermelon(variety, weight, sweetness, ripeness, price, organic, supplier)
                print("✅ Арбуз успешно добавлен!")
            except ValueError:
                print("❌ Ошибка: проверьте правильность введенных данных!")
                
        elif choice == "9":
            try:
                wm_id = int(input("ID арбуза для обновления: "))
                print("Введите новые данные (оставьте пустым для сохранения текущего значения):")
                
                updates = {}
                variety = input("Сорт: ")
                if variety: updates['variety'] = variety
                
                weight = input("Вес (кг): ")
                if weight: updates['weight'] = float(weight)
                
                sweetness = input("Сладость (1-10): ")
                if sweetness: updates['sweetness'] = int(sweetness)
                
                ripeness = input("Спелость: ")
                if ripeness: updates['ripeness'] = ripeness
                
                price = input("Цена за кг: ")
                if price: updates['price'] = float(price)
                
                organic = input("Органический (да/нет): ")
                if organic: updates['is_organic'] = organic.lower() == "да"
                
                supplier = input("Поставщик: ")
                if supplier: updates['supplier'] = supplier
                
                if updates:
                    crud.update_watermelon(wm_id, **updates)
                else:
                    print("ℹ️  Не введено новых данных.")
                    
            except (ValueError, TypeError):
                print("❌ Ошибка: проверьте правильность введенных данных!")
                
        elif choice == "10":
            try:
                wm_id = int(input("ID арбуза для удаления: "))
                if crud.delete_watermelon(wm_id):
                    print("✅ Арбуз удален!")
                else:
                    print("❌ Арбуз с таким ID не найден!")
            except ValueError:
                print("❌ Ошибка: введите корректный ID!")
                
        elif choice == "0":
            print("👋 До свидания!")
            crud.close()
            sys.exit()
            
        else:
            print("❌ Неверный выбор! Попробуйте снова.")

if __name__ == "__main__":
    main()