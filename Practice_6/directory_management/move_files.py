import shutil
import os

os.makedirs("destination", exist_ok=True)

# create sample file
with open("move_example.txt", "w") as f:
    f.write("This file will be copied and moved.")

# copy file
shutil.copy("move_example.txt", "destination/move_example_copy.txt")
print("File copied")

# move file
shutil.move("move_example.txt", "destination/move_example_moved.txt")
print("File moved")