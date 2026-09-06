import os

source_path = r"C:\Users\taigb\Downloads\Video"

for file_name in os.listdir(source_path):
    if file_name.startswith("The Art of Sarah"):
        old_path = os.path.join(source_path, file_name)

        new_name = os.path.splitext(file_name)[1]

        for letter in new_name:
            print(letter, "")