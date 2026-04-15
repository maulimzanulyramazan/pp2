class person():
    name = ""
    GPA = 0.0
student = person()
a = input().split()
student.name = a[0]
student.GPA = float(a[1])
print(f"Student: {student.name}, GPA: {student.GPA}")