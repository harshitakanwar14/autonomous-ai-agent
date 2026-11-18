
from tools.file_writer import write_file

result = write_file(
    "test_report.txt",
    "This is my first report."
)

print("First write:", result)

result = write_file(
    "test_report.txt",
    "This is my updated report."
)

print("Second write:", result)
