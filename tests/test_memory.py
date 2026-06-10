import unittest

from src.db.backend.memory import MemoryDatabase
from src.db.backend.errors import (
    TableAlreadyExistsError,
    MissingColumnError,
    UnknownColumnError,
)


class TestMemoryDatabase(unittest.TestCase):

    def setUp(self):
        self.db = MemoryDatabase()
        self.db.create_table("students", ("id", "first_name", "second_name", "age", "sex"))

        self.test_records = [
            {"id": 1, "first_name": "John", "second_name": "Doe", "age": 20, "sex": "M"},
            {"id": 2, "first_name": "Jane", "second_name": "Smith", "age": 22, "sex": "F"},
            {"id": 3, "first_name": "Alice", "second_name": "Johnson", "age": 19, "sex": "F"},
            {"id": 4, "first_name": "Bob", "second_name": "Brown", "age": 21, "sex": "M"},
            {"id": 5, "first_name": "Charlie", "second_name": "Davis", "age": 18, "sex": "M"},
        ]

        for record in self.test_records:
            self.db.insert_record("students", record)

    def test_table_exists(self):
        self.assertTrue(self.db.table_exists("students"))
        self.assertFalse(self.db.table_exists("missing"))

    def test_create_table(self):
        self.db.create_table("new_table", ("id", "name"))
        self.assertTrue(self.db.table_exists("new_table"))

    def test_create_table_already_exists(self):
        with self.assertRaises(TableAlreadyExistsError):
            self.db.create_table("students", ("id", "name"))

    def test_insert_record_success(self):
        record = {"id": 6, "first_name": "Eve", "second_name": "Miller", "age": 23, "sex": "F"}
        self.db.insert_record("students", record)

        records = self.db.select_records("students", id=6)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["first_name"], "Eve")

    def test_insert_record_missing_column(self):
        with self.assertRaises(MissingColumnError):
            self.db.insert_record("students", {"id": 6, "first_name": "Eve"})

    def test_insert_record_unknown_column(self):
        with self.assertRaises(UnknownColumnError):
            self.db.insert_record(
                "students",
                {
                    "id": 6,
                    "first_name": "Eve",
                    "second_name": "Miller",
                    "age": 23,
                    "sex": "F",
                    "unknown": "x"
                }
            )

    def test_select_records_no_filters(self):
        records = self.db.select_records("students")
        self.assertEqual(len(records), 5)

    def test_select_records_by_id(self):
        records = self.db.select_records("students", id=1)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["first_name"], "John")

    def test_select_records_by_first_name(self):
        records = self.db.select_records("students", first_name="Jane")
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["id"], 2)

    def test_select_records_by_age(self):
        records = self.db.select_records("students", age=20)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["id"], 1)

    def test_select_records_by_sex(self):
        records = self.db.select_records("students", sex="F")
        self.assertEqual(len(records), 2)

    def test_select_records_multiple_filters(self):
        records = self.db.select_records("students", sex="M", age=21)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["id"], 4)

    def test_select_records_unknown_filter(self):
        with self.assertRaises(UnknownColumnError):
            self.db.select_records("students", unknown="value")

    def test_update_record_success(self):
        updated = self.db.update_record("students", 1, "id", first_name="Jonathan", age=21)
        self.assertEqual(updated["first_name"], "Jonathan")
        self.assertEqual(updated["age"], 21)

    def test_update_record_not_found(self):
        result = self.db.update_record("students", 999, "id", first_name="Nobody")
        self.assertIsNone(result)

    def test_delete_record_success(self):
        deleted = self.db.delete_record("students", 1, "id")
        self.assertEqual(deleted["first_name"], "John")
        self.assertEqual(len(self.db.get_all_records("students")), 4)

    def test_delete_record_not_found(self):
        result = self.db.delete_record("students", 999, "id")
        self.assertIsNone(result)

    def test_get_all_records(self):
        records = self.db.get_all_records("students")
        self.assertEqual(len(records), 5)

    def test_count_records(self):
        count = self.db.count_records("students")
        self.assertEqual(count, 5)


if __name__ == "__main__":
    unittest.main()