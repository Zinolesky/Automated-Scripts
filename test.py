import os
import shutil

source_path = r"C:/Users/taigb/Downloads/Video"

for file_name in os.listdir(source_path):
    if file_name.startswith("The Art of Sarah"):
        old_path = os.path.join(source_path, file_name)

        new_name = file_name + "1"
        new_path = os.path.join(source_path, new_name)

        os.rename(old_path, new_path)