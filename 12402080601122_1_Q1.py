def average_marks(marks):
    return sum(marks) / len(marks)


print("Campus Merit Analyzer")
print("Enter n, k and m:")
n, k, m = map(int, input().split())

students = []

print("Enter student details:")
print("Format: enrollment name semester cpi mark1 mark2 ...")

for i in range(n):
    print(f"Student {i + 1}:")
    data = input().split()

    enrollment = data[0]
    name = data[1]
    semester = int(data[2])
    cpi = float(data[3])
    marks = tuple(map(int, data[4:]))

    # Check student data before adding it
    if len(marks) != m or not 1 <= semester <= 8 or not 0 <= cpi <= 10:
        print("Invalid input")
        raise SystemExit

    if any(mark < 0 or mark > 100 for mark in marks):
        print("Invalid marks")
        raise SystemExit

    students.append((enrollment, name, semester, cpi, marks))
# Group students semester-wise
semester_students = {}

for student in students:
    semester = student[2]

    if semester not in semester_students:
        semester_students[semester] = []

    semester_students[semester].append(student)

print()
print("Result:")
# Sort students using CPI, average marks and enrollment
for semester in sorted(semester_students):
    group = semester_students[semester]

    group.sort(
        key=lambda student: (
            -student[3],
            -average_marks(student[4]),
            student[0]
        )
    )

    print(
        f"Semester {semester}:",
        *[student[0] for student in group[:k]]
    )

for subject in range(m):
    highest = max(student[4][subject] for student in students)

    toppers = [
        student[0]
        for student in students
        if student[4][subject] == highest
    ]

    toppers.sort()
    print(f"S{subject + 1}:", *toppers)
