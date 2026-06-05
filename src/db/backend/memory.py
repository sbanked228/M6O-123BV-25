type StudentRecord = tuple[int, str, int, str]

students: list[StudentRecord] = []

next_id = 1

def create_record(name: str, age: int, group: str) -> StudentRecord:

    global next_id
    
    if age < 0 or age > 120:
        raise ValueError("Возраст должен быть от 0 до 120")
    
    if not name or not name.strip():
        raise ValueError("Имя не может быть пустым")
    
    new_record = (next_id, name.strip(), age, group.strip())
    
    students.append(new_record)
    
    next_id += 1
    
    return new_record

def select_record(
    student_id: int | None = None,
    name: str | None = None,
    age: int | None = None,
    group: str | None = None
) -> list[StudentRecord]:

    if student_id is None and name is None and age is None and group is None:
        return students.copy()
    
    result = []

    for record in students:
        if student_id is not None and record[0] != student_id:
            continue
        if name is not None and record[1] != name:
            continue
        if age is not None and record[2] != age:
            continue
        if group is not None and record[3] != group:
            continue
        
        result.append(record)
    
    return result

def update_record(
    student_id: int,
    name: str | None = None,
    age: int | None = None,
    group: str | None = None
) -> StudentRecord:

    for i, record in enumerate(students):
        if record[0] == student_id:
            new_record = (
                record[0],
                name if name is not None else record[1],
                age if age is not None else record[2],
                group if group is not None else record[3]
            )
            students[i] = new_record
            return new_record
    
    raise ValueError(f"Студент с ID {student_id} не найден")

def delete_record(student_id: int) -> StudentRecord:
    for i, record in enumerate(students):
        if record[0] == student_id:
            return students.pop(i)
    
    raise ValueError(f"Студент с ID {student_id} не найден")