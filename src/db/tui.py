from src.db.backend.file import FileDatabase
from src.db.backend.memory import MemoryDatabase
from src.db.backend.errors import (
    TableAlreadyExistsError,
    TableNotFoundError,
    MissingColumnError,
    UnknownColumnError,
    InvalidStorageDataError,
    InvalidAgeError,
    DuplicateIDError,
    RecordNotFoundError,
)


class StudentUI:

    def __init__(self):
        self.database = self._select_database_type()
        self.current_table = "students"

        if not self.database.table_exists(self.current_table):
            self.database.create_table(
                self.current_table,
                ("id", "first_name", "second_name", "age", "sex")
            )

        self.next_id = self._get_next_id()

    def _select_database_type(self):
        print("\n" + "=" * 40)
        print("ВЫБОР ТИПА БАЗЫ ДАННЫХ".center(40))
        print("=" * 40)
        print("1. In-memory (данные не сохраняются)")
        print("2. File (данные сохраняются в JSON-файлы)")
        print("-" * 40)

        while True:
            choice = input("Выберите тип (1 или 2): ").strip()
            if choice == "1":
                print("\n Выбрана in-memory база данных.")
                return MemoryDatabase()
            elif choice == "2":
                print("\n Выбрана файловая база данных (данные будут сохранены в папке 'data/').")
                return FileDatabase()
            else:
                print("Ошибка: введите 1 или 2.")

    def _get_next_id(self) -> int:
        records = self.database.get_all_records(self.current_table)
        if not records:
            return 1
        max_id = max(record.get("id", 0) for record in records)
        return max_id + 1

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

        first_name = input("Имя: ").strip()
        second_name = input("Фамилия: ").strip()
        age = self._read_int("Возраст: ")
        sex = input("Пол (M/F): ").strip().upper()

        if age < 0 or age > 120:
            print("Ошибка: возраст должен быть от 0 до 120.")
            return

        if sex not in ("M", "F"):
            print("Ошибка: пол должен быть M или F.")
            return

        try:
            self.database.insert_record(
                self.current_table,
                {
                    "id": student_id,
                    "first_name": first_name,
                    "second_name": second_name,
                    "age": age,
                    "sex": sex,
                }
            )
            self.next_id += 1
            print(f"Студент добавлен! ID = {student_id}")
        except (MissingColumnError, UnknownColumnError, TableNotFoundError) as e:
            print(f"Ошибка: {e}")

    def _show_all_students(self):
        print("\n --- ВСЕ СТУДЕНТЫ ---")

        try:
            records = self.database.get_all_records(self.current_table)
        except TableNotFoundError as e:
            print(f"Ошибка: {e}")
            return

        if not records:
            print("Список пуст.")
            return

        print(f"\n{'ID':<5} {'Имя':<12} {'Фамилия':<12} {'Возраст':<8} {'Пол':<5}")
        print("-" * 50)
        for r in records:
            print(f"{r['id']:<5} {r['first_name']:<12} {r['second_name']:<12} {r['age']:<8} {r['sex']:<5}")

    def _find_students(self):
        print("\n--- ПОИСК СТУДЕНТОВ ---")
        print("(оставьте поле пустым, чтобы пропустить фильтр)")

        filters = {}
        id_val = self._read_optional_int("ID: ")
        if id_val is not None:
            filters["id"] = id_val

        first_name = input("Имя: ").strip()
        if first_name:
            filters["first_name"] = first_name

        second_name = input("Фамилия: ").strip()
        if second_name:
            filters["second_name"] = second_name

        age = self._read_optional_int("Возраст: ")
        if age is not None:
            filters["age"] = age

        sex = input("Пол (M/F): ").strip().upper()
        if sex:
            filters["sex"] = sex

        try:
            records = self.database.select_records(self.current_table, **filters)
        except (UnknownColumnError, TableNotFoundError) as e:
            print(f"Ошибка: {e}")
            return

        if not records:
            print("Студенты не найдены.")
            return

        print(f"\n Найдено {len(records)} записей:")
        for r in records:
            print(f"  ID={r['id']}, {r['first_name']} {r['second_name']}, {r['age']} лет, пол {r['sex']}")

    def _update_student(self):
        print("\n--- ОБНОВЛЕНИЕ ДАННЫХ ---")

        student_id = self._read_int("ID студента для обновления: ")

        print("(оставьте поле пустым, чтобы не менять)")
        first_name = input("Новое имя: ").strip()
        second_name = input("Новая фамилия: ").strip()
        age_str = input("Новый возраст: ").strip()
        sex = input("Новый пол (M/F): ").strip().upper()

        updates = {}
        if first_name:
            updates["first_name"] = first_name
        if second_name:
            updates["second_name"] = second_name
        if age_str:
            try:
                updates["age"] = int(age_str)
            except ValueError:
                print("Ошибка: возраст должен быть числом.")
                return
        if sex:
            if sex not in ("M", "F"):
                print("Ошибка: пол должен быть M или F.")
                return
            updates["sex"] = sex

        if not updates:
            print("Нет данных для обновления.")
            return

        try:
            result = self.database.update_record(self.current_table, student_id, "id", **updates)
            if result:
                print(f"Данные обновлены: {result}")
            else:
                print(f"Студент с ID {student_id} не найден.")
        except (TableNotFoundError, UnknownColumnError) as e:
            print(f"Ошибка: {e}")

    def _delete_student(self):
        print("\n--- УДАЛЕНИЕ СТУДЕНТА ---")

        student_id = self._read_int("ID студента для удаления: ")

        try:
            result = self.database.delete_record(self.current_table, student_id, "id")
            if result:
                print(f"Удалён студент: {result}")
            else:
                print(f"Студент с ID {student_id} не найден.")
        except TableNotFoundError as e:
            print(f"Ошибка: {e}")