class DatabaseError(Exception):
    pass


class TableAlreadyExistsError(DatabaseError):
    pass


class TableNotFoundError(DatabaseError):
    pass


class MissingColumnError(DatabaseError):
    pass


class UnknownColumnError(DatabaseError):
    pass


class InvalidStorageDataError(DatabaseError):
    pass


# Старые исключения (для обратной совместимости)
class StudentTableError(DatabaseError):
    pass


class InvalidAgeError(StudentTableError):
    pass


class DuplicateIDError(StudentTableError):
    pass


class RecordNotFoundError(StudentTableError):
    pass