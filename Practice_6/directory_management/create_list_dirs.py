import os

# create nested directories
os.makedirs("test_folder/subfolder", exist_ok=True)
print("Nested directories created")

# list files and folders
print("Files and folders in current directory:")
for item in os.listdir("."):
    print(item)

# find .py files
print("\nPython files:")
for item in os.listdir("."):
    if item.endswith(".py"):
        print(item)