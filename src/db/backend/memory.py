from .errors import DuplicateIDError, InvalidAgeError, RecordNotFoundError

type StudentRecord = tuple[int, str, str, int, str]


class StudentTable:

    def __init__(self) -> None:
        self._students: list[StudentRecord] = []

    def create_record(
        self,
        student_id: int,
        first_name: str,
        second_name: str,
        age: int,
        sex: str,
    ) -> StudentRecord:
        if age < 0:
            raise InvalidAgeError("Поле age не может быть отрицательным.")

        if any(record[0] == student_id for record in self._students):
            raise DuplicateIDError(f"Запись с id={student_id} уже существует.")

        new_record: StudentRecord = (
            student_id,
            first_name.strip(),
            second_name.strip(),
            age,
            sex.strip(),
        )
        self._students.append(new_record)
        return new_record

    def select_record(
        self,
        student_id: int | None = None,
        first_name: str | None = None,
        second_name: str | None = None,
        age: int | None = None,
        sex: str | None = None,
    ) -> list[StudentRecord]:
        if all(param is None for param in [student_id, first_name, second_name, age, sex]):
            return self._students.copy()

        result: list[StudentRecord] = []

        for record in self._students:
            if student_id is not None and record[0] != student_id:
                continue
            if first_name is not None and record[1] != first_name:
                continue
            if second_name is not None and record[2] != second_name:
                continue
            if age is not None and record[3] != age:
                continue
            if sex is not None and record[4] != sex:
                continue
            result.append(record)

        return result

    def update_record(
        self,
        student_id: int,
        first_name: str | None = None,
        second_name: str | None = None,
        age: int | None = None,
        sex: str | None = None,
    ) -> StudentRecord:
        for i, record in enumerate(self._students):
            if record[0] == student_id:
                new_record: StudentRecord = (
                    student_id,
                    first_name.strip() if first_name is not None else record[1],
                    second_name.strip() if second_name is not None else record[2],
                    age if age is not None else record[3],
                    sex.strip() if sex is not None else record[4],
                )
                self._students[i] = new_record
                return new_record

        raise RecordNotFoundError(f"Запись с id={student_id} не найдена.")

    def delete_record(self, student_id: int) -> StudentRecord:
        for i, record in enumerate(self._students):
            if record[0] == student_id:
                return self._students.pop(i)

        raise RecordNotFoundError(f"Запись с id={student_id} не найдена.")

    def get_all_records(self) -> list[StudentRecord]:
        return self._students.copy()

    def count_records(self) -> int:
        return len(self._students)