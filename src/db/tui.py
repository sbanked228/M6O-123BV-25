from src.db.backend.memory import StudentTable
from src.db.backend.errors import (
    InvalidAgeError,
    DuplicateIDError,
    RecordNotFoundError,
)


class StudentUI:

    def __init__(self):
        self.table = StudentTable()
        self.next_id = 1

    def run(self):
        while True:
            self._print_menu()
            choice = input("Выберите действие: ").strip()

            if choice == "1":
                self._add_student()
            elif choice == "2":
                self._show_all_students()
            elif choice == "3":
                self._find_students()
            elif choice == "4":
                self._update_student()
            elif choice == "5":
                self._delete_student()
            elif choice == "0":
                print("До свидания!")
                break
            else:
                print("Неизвестная команда. Попробуйте снова.")

    def _print_menu(self):
        print("\n" + "=" * 40)
        print("БАЗА ДАННЫХ СТУДЕНТОВ".center(40))
        print("=" * 40)
        print("1. Добавить студента")
        print("2. Показать всех студентов")
        print("3. Найти студента")
        print("4. Обновить данные студента")
        print("5. Удалить студента")
        print("0. Выход")
        print("-" * 40)

    def _read_int(self, prompt: str) -> int:
        while True:
            try:
                return int(input(prompt).strip())
            except ValueError:
                print("Ошибка: введите целое число.")

    def _read_optional_int(self, prompt: str) -> int | None:
        value = input(prompt).strip()
        if value == "":
            return None
        try:
            return int(value)
        except ValueError:
            print("Ошибка: введите целое число или оставьте поле пустым.")
            return None

    def _add_student(self):
        print("\n--- ДОБАВЛЕНИЕ СТУДЕНТА ---")
        
        student_id = self.next_id
        print(f"ID: {student_id} (автоматически)")
        
        name = input("Имя: ").strip()
        surname = input("Фамилия: ").strip()
        age = self._read_int("Возраст: ")
        sex = input("Пол (M/F): ").strip().upper()

        try:
            record = self.table.create_record(student_id, name, surname, age, sex)
            self.next_id += 1
            print(f"Студент добавлен: {record}")
        except (InvalidAgeError, DuplicateIDError) as e:
            print(f"Ошибка: {e}")

    def _show_all_students(self):
        print("\n--- ВСЕ СТУДЕНТЫ ---")
        records = self.table.get_all_records()

        if not records:
            print("Список пуст.")
            return

        print(f"{'ID':<5} {'Имя':<12} {'Фамилия':<12} {'Возраст':<8} {'Пол':<5}")
        print("-" * 50)
        for r in records:
            print(f"{r[0]:<5} {r[1]:<12} {r[2]:<12} {r[3]:<8} {r[4]:<5}")

    def _find_students(self):
        print("\n--- ПОИСК СТУДЕНТОВ ---")
        print("(оставьте поле пустым, чтобы пропустить фильтр)")

        student_id = self._read_optional_int("ID: ")
        name = input("Имя: ").strip() or None
        surname = input("Фамилия: ").strip() or None
        age = self._read_optional_int("Возраст: ")
        sex = input("Пол (M/F): ").strip().upper() or None

        records = self.table.select_record(
            student_id=student_id,
            first_name=name,
            second_name=surname,
            age=age,
            sex=sex,
        )

        if not records:
            print("Студенты не найдены.")
            return

        print(f"\nНайдено {len(records)} записей:")
        for r in records:
            print(f"  ID={r[0]}, {r[1]} {r[2]}, {r[3]} лет, пол {r[4]}")

    def _update_student(self):
        print("\n--- ОБНОВЛЕНИЕ ДАННЫХ ---")
        
        student_id = self._read_int("ID студента для обновления: ")
        
        print("(оставьте поле пустым, чтобы не менять)")
        name = input("Новое имя: ").strip() or None
        surname = input("Новая фамилия: ").strip() or None
        age_str = input("Новый возраст: ").strip()
        age = int(age_str) if age_str else None
        sex = input("Новый пол (M/F): ").strip().upper() or None

        try:
            record = self.table.update_record(student_id, name, surname, age, sex)
            print(f"Данные обновлены: {record}")
        except RecordNotFoundError as e:
            print(f"Ошибка: {e}")

    def _delete_student(self):
        print("\n--- УДАЛЕНИЕ СТУДЕНТА ---")
        
        student_id = self._read_int("ID студента для удаления: ")

        try:
            record = self.table.delete_record(student_id)
            print(f"Удалён студент: {record}")
        except RecordNotFoundError as e:
            print(f"Ошибка: {e}")