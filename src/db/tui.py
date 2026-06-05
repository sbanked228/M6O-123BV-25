from .backend.memory import create_record, select_record, update_record, delete_record

def run():
    while True:
        print("\n" + "="*40)
        print("        БАЗА ДАННЫХ СТУДЕНТОВ")
        print("="*40)
        print("1. Добавить студента")
        print("2. Показать всех студентов")
        print("3. Найти студента")
        print("4. Обновить данные студента") 
        print("5. Удалить студента")          
        print("0. Выход")
        print("-"*40)
        
        choice = input("Выберите действие: ").strip()
        
        if choice == "1":
            add_student()
        elif choice == "2":
            show_all_students()
        elif choice == "3":
            find_students()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Ошибка: неверный выбор. Попробуйте снова.")

def add_student():
    print("\n--- ДОБАВЛЕНИЕ СТУДЕНТА ---")
    
    name = input("Имя: ").strip()

    while True:
        try:
            age = int(input("Возраст: "))
            break
        except ValueError:
            print("Ошибка: введите число!")
    
    group = input("Группа: ").strip()
    
    try:
        record = create_record(name, age, group)
        print(f" Студент добавлен! ID = {record[0]}")
    except ValueError as e:
        print(f" Ошибка: {e}")

def show_all_students():
    print("\n--- ВСЕ СТУДЕНТЫ ---")
    records = select_record()
    
    if not records:
        print("Список пуст.")
        return
    
    print(f"{'ID':<5} {'Имя':<15} {'Возраст':<8} {'Группа':<10}")
    print("-" * 40)
    for record in records:
        print(f"{record[0]:<5} {record[1]:<15} {record[2]:<8} {record[3]:<10}")

def find_students():
    print("\n--- ПОИСК СТУДЕНТОВ ---")
    print("(оставьте поле пустым, чтобы пропустить фильтр)")
    
    id_input = input("ID: ").strip()
    student_id = int(id_input) if id_input else None
    
    name = input("Имя: ").strip() or None
    
    age_input = input("Возраст: ").strip()
    age = int(age_input) if age_input else None
    
    group = input("Группа: ").strip() or None
    
    records = select_record(
        student_id=student_id,
        name=name,
        age=age,
        group=group
    )
    
    if not records:
        print("Студенты не найдены.")
        return
    
    print(f"\nНайдено {len(records)} записей:")
    for record in records:
        print(f"  ID={record[0]}, {record[1]}, {record[2]} лет, группа {record[3]}")

def update_student():
    print("\n--- ОБНОВЛЕНИЕ ДАННЫХ ---")
    
    try:
        student_id = int(input("ID студента для обновления: "))
    except ValueError:
        print("Ошибка: ID должно быть числом")
        return
    
    print("(оставьте поле пустым, чтобы не менять)")
    name = input("Новое имя: ").strip() or None
    
    age_input = input("Новый возраст: ").strip()
    age = int(age_input) if age_input else None
    
    group = input("Новая группа: ").strip() or None
    
    try:
        record = update_record(student_id, name, age, group)
        print(f" Данные обновлены: {record}")
    except ValueError as e:
        print(f" Ошибка: {e}")

def delete_student():
    print("\n--- УДАЛЕНИЕ СТУДЕНТА ---")
    
    try:
        student_id = int(input("ID студента для удаления: "))
    except ValueError:
        print("Ошибка: ID должно быть числом")
        return
    
    try:
        record = delete_record(student_id)
        print(f" Удалён студент: {record}")
    except ValueError as e:
        print(f" Ошибка: {e}")