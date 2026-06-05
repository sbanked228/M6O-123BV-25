import unittest
from src.db.backend.memory import StudentTable
from src.db.backend.errors import (
    InvalidAgeError,
    DuplicateIDError,
    RecordNotFoundError,
)


class TestStudentTable(unittest.TestCase):

    def setUp(self):
        self.table = StudentTable()
        self.test_records = [
            (1, "John", "Doe", 20, "M"),
            (2, "Jane", "Smith", 22, "F"),
            (3, "Alice", "Johnson", 19, "F"),
            (4, "Bob", "Brown", 21, "M"),
            (5, "Charlie", "Davis", 18, "M"),
        ]
        for record in self.test_records:
            self.table.create_record(*record)

    def test_initialization(self):
        new_table = StudentTable()
        self.assertIsInstance(new_table, StudentTable)
        self.assertEqual(new_table.count_records(), 0)

    def test_create_record_success(self):
        new_record = self.table.create_record(6, "Eve", "Miller", 23, "F")
        self.assertEqual(new_record[0], 6)
        self.assertEqual(new_record[1], "Eve")
        self.assertEqual(new_record[4], "F")
        self.assertEqual(self.table.count_records(), 6)

    def test_create_record_negative_age(self):
        with self.assertRaises(InvalidAgeError):
            self.table.create_record(6, "Eve", "Miller", -5, "F")

    def test_create_record_duplicate_id(self):
        with self.assertRaises(DuplicateIDError):
            self.table.create_record(1, "Eve", "Miller", 23, "F")

    def test_select_record_no_filters(self):
        result = self.table.select_record()
        self.assertEqual(len(result), 5)
        self.assertEqual(result, self.test_records)

    def test_select_record_by_id(self):
        result = self.table.select_record(student_id=1)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], self.test_records[0])

    def test_select_record_by_first_name(self):
        result = self.table.select_record(first_name="Jane")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], self.test_records[1])

    def test_select_record_by_age(self):
        result = self.table.select_record(age=20)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], self.test_records[0])

    def test_select_record_by_sex(self):
        result = self.table.select_record(sex="F")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], self.test_records[1])
        self.assertEqual(result[1], self.test_records[2])

    def test_select_record_multiple_filters(self):
        result = self.table.select_record(sex="M", age=21)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], self.test_records[3])

    def test_update_record_success(self):
        updated = self.table.update_record(1, first_name="Jonathan", age=21)
        self.assertEqual(updated[1], "Jonathan")
        self.assertEqual(updated[2], "Doe")
        self.assertEqual(updated[3], 21)

        record = self.table.select_record(student_id=1)[0]
        self.assertEqual(record[1], "Jonathan")

    def test_update_record_not_found(self):
        with self.assertRaises(RecordNotFoundError):
            self.table.update_record(999, first_name="Nobody")

    def test_delete_record_success(self):
        deleted = self.table.delete_record(1)
        self.assertEqual(deleted, self.test_records[0])
        self.assertEqual(self.table.count_records(), 4)

        result = self.table.select_record(student_id=1)
        self.assertEqual(len(result), 0)

    def test_delete_record_not_found(self):
        with self.assertRaises(RecordNotFoundError):
            self.table.delete_record(999)

    def test_get_all_records(self):
        all_records = self.table.get_all_records()
        self.assertEqual(all_records, self.test_records)

        all_records.append((99, "Test", "User", 99, "X"))
        self.assertEqual(self.table.count_records(), 5)

    def test_count_records(self):
        self.assertEqual(self.table.count_records(), 5)
        self.table.create_record(6, "Eve", "Miller", 23, "F")
        self.assertEqual(self.table.count_records(), 6)
        self.table.delete_record(1)
        self.assertEqual(self.table.count_records(), 5)


if __name__ == "__main__":
    unittest.main()