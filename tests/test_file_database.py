import tempfile
import unittest
import json
from pathlib import Path

from src.db.backend.file import FileDatabase
from src.db.backend.errors import (
    TableNotFoundError,
    TableAlreadyExistsError,
    InvalidStorageDataError,
)


class TestFileDatabase(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db = FileDatabase(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_create_table(self):
        self.db.create_table("test_table", ("id", "name"))
        self.assertTrue(self.db.table_exists("test_table"))

    def test_create_table_already_exists(self):
        self.db.create_table("test_table", ("id", "name"))
        with self.assertRaises(TableAlreadyExistsError):
            self.db.create_table("test_table", ("id", "name"))

    def test_insert_and_select_record(self):
        self.db.create_table("test_table", ("id", "name"))
        self.db.insert_record("test_table", {"id": 1, "name": "John"})

        records = self.db.select_records("test_table")
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["name"], "John")

    def test_select_with_filters(self):
        self.db.create_table("test_table", ("id", "name"))
        self.db.insert_record("test_table", {"id": 1, "name": "John"})
        self.db.insert_record("test_table", {"id": 2, "name": "Jane"})

        records = self.db.select_records("test_table", name="Jane")
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["id"], 2)

    def test_select_from_missing_table(self):
        with self.assertRaises(TableNotFoundError):
            self.db.select_records("missing_table")

    def test_data_persists_between_instances(self):
        db1 = FileDatabase(self.temp_dir.name)
        db1.create_table("test_table", ("id", "name"))
        db1.insert_record("test_table", {"id": 1, "name": "John"})

        db2 = FileDatabase(self.temp_dir.name)
        records = db2.select_records("test_table")

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["name"], "John")

    def test_update_record(self):
        self.db.create_table("test_table", ("id", "name", "age"))
        self.db.insert_record("test_table", {"id": 1, "name": "John", "age": 20})

        updated = self.db.update_record("test_table", 1, "id", age=21)
        self.assertEqual(updated["age"], 21)

        records = self.db.select_records("test_table", id=1)
        self.assertEqual(records[0]["age"], 21)

    def test_delete_record(self):
        self.db.create_table("test_table", ("id", "name"))
        self.db.insert_record("test_table", {"id": 1, "name": "John"})

        deleted = self.db.delete_record("test_table", 1, "id")
        self.assertEqual(deleted["name"], "John")

        records = self.db.select_records("test_table")
        self.assertEqual(len(records), 0)

    def test_invalid_json_file(self):
        self.db.create_table("test_table", ("id", "name"))

        table_path = Path(self.temp_dir.name) / "test_table.json"
        with open(table_path, "w", encoding="utf-8") as f:
            f.write("{invalid json}")

        with self.assertRaises(InvalidStorageDataError):
            self.db.select_records("test_table")


if __name__ == "__main__":
    unittest.main()