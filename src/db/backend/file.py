import json
from pathlib import Path
from typing import Any

from .database import Database
from .errors import InvalidStorageDataError, TableNotFoundError, FileOperationError
from .table import Table


class FileDatabase(Database):

    def __init__(self, directory: str = "data") -> None:
        self.directory = Path(directory)
        try:
            self.directory.mkdir(parents=True, exist_ok=True)
        except OSError as error:
            raise FileOperationError(
                f"Не удалось создать каталог для данных '{directory}': {error}"
            ) from error
    
    def _get_table_path(self, table_name: str) -> Path:
        return self.directory / f"{table_name}.json"

    def _table_exists(self, table_name: str) -> bool:
        return self._get_table_path(table_name).exists()

    def _serialize_table(self, table: Table) -> dict[str, Any]:
        return {
            "columns": list(table.columns),
            "records": [record.copy() for record in table.records],
        }

    def _deserialize_table(self, data: dict[str, Any]) -> Table:
        if "columns" not in data:
            raise InvalidStorageDataError(
            )
        if "records" not in data:
            raise InvalidStorageDataError(
            )
        
        if not isinstance(data["columns"], list):
            raise InvalidStorageDataError(
                f"Поле 'columns' должно быть списком, получено: {type(data['columns']).__name__}"
            )
        
        if not isinstance(data["records"], list):
            raise InvalidStorageDataError(
                f"Поле 'records' должно быть списком, получено: {type(data['records']).__name__}"
            )
        
        for i, col in enumerate(data["columns"]):
            if not isinstance(col, str):
                raise InvalidStorageDataError(
                    f"Элемент columns[{i}] должен быть строкой, получено: {type(col).__name__}"
                )
        
        for i, record in enumerate(data["records"]):
            if not isinstance(record, dict):
                raise InvalidStorageDataError(
                    f"Элемент records[{i}] должен быть словарём, получено: {type(record).__name__}"
                )
        
        columns = tuple(data["columns"])
        records = data["records"]
        return Table(columns, records)

    def _load_table(self, table_name: str) -> Table:
        table_path = self._get_table_path(table_name)

        if not table_path.exists():
            raise TableNotFoundError(f"Таблица '{table_name}' не существует.")

        try:
            with table_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError as error:
            raise InvalidStorageDataError(
                f"Файл таблицы '{table_name}' содержит некорректный JSON."
            ) from error
        except OSError as error:
            raise FileOperationError(
                f"Не удалось прочитать файл таблицы '{table_name}': {error}"
            ) from error

        return self._deserialize_table(data)

    def _save_table(self, table_name: str, table: Table) -> None:
        table_path = self._get_table_path(table_name)

        try:
            with table_path.open("w", encoding="utf-8") as file:
                json.dump(
                    self._serialize_table(table),
                    file,
                    ensure_ascii=False,
                    indent=2,
                )
        except OSError as error:
            raise FileOperationError(
                f"Не удалось записать файл таблицы '{table_name}': {error}"
            ) from error   