import os

# 1. append new line
with open("sample.txt", "a") as f:
    f.write("New appended line\n")

# 2. verify content
with open("sample.txt", "r") as f:
    print("Updated content:")
    print(f.read())

# 3. COPY FILE (shutil.copy орнына)
with open("sample.txt", "r") as src:
    data = src.read()

with open("backup_sample.txt", "w") as dest:
    dest.write(data)

print("File copied")

# 4. delete safely (os қолданамыз)
if os.path.exists("backup_sample.txt"):
    os.remove("backup_sample.txt")
    print("File deleted safely")
else:
    print("File does not exist")