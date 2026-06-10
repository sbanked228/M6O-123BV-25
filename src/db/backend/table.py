from typing import Any

from .errors import MissingColumnError, UnknownColumnError, InvalidAgeError


class Table:

    def _validate_record(self, record: dict[str, Any]) -> None:
        missing_columns = [column for column in self.columns if column not in record]
        if missing_columns:
            raise MissingColumnError(
                f"Отсутствует поле '{missing_columns[0]}' в записи."
            )
        
        extra_columns = [column for column in record if column not in self.columns]
        if extra_columns:
            raise UnknownColumnError(
                f"Поле '{extra_columns[0]}' не определено в структуре таблицы."
            )
        
        if "age" in self.columns and "age" in record:
            age = record["age"]
            if not isinstance(age, int) or age < 0 or age > 120:
                raise InvalidAgeError(f"Некорректный возраст: {age}. Должен быть от 0 до 120.")

    def __init__(self, columns: tuple[str, ...], records: list[dict[str, Any]] | None = None) -> None:
        self.columns = columns
        self.records: list[dict[str, Any]] = []

        if records is not None:
            for record in records:
                self.insert_record(record)

    def insert_record(self, record: dict[str, Any]) -> None:
        self._validate_record(record)
        self.records.append(record.copy())

    def select_records(self, **filters: Any) -> list[dict[str, Any]]:
        unknown_filters = [key for key in filters if key not in self.columns]
        if unknown_filters:
            raise UnknownColumnError(
                f"Поле '{unknown_filters[0]}' не определено в структуре таблицы."
            )

        if not filters:
            return [record.copy() for record in self.records]

        result: list[dict[str, Any]] = []
        for record in self.records:
            if all(record.get(key) == value for key, value in filters.items()):
                result.append(record.copy())

        return result

    def update_record(self, record_id: int, id_column: str = "id", **updates: Any) -> dict[str, Any] | None:
        for i, record in enumerate(self.records):
            if record.get(id_column) == record_id:
                for key in updates:
                    if key not in self.columns:
                        raise UnknownColumnError(
                            f"Поле '{key}' не определено в структуре таблицы."
                        )
                
                updated_record = record.copy()
                updated_record.update(updates)
                
                self._validate_record(updated_record)
                
                self.records[i] = updated_record
                return updated_record
        return None

    def delete_record(self, record_id: int, id_column: str = "id") -> dict[str, Any] | None:
        for i, record in enumerate(self.records):
            if record.get(id_column) == record_id:
                return self.records.pop(i)
        return None

    def get_all_records(self) -> list[dict[str, Any]]:
        return [record.copy() for record in self.records]

    def count_records(self) -> int:
        return len(self.records)