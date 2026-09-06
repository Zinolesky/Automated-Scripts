import os
import shutil

source_folder_path = input("Source folder name: C:\\Users\\taigb\\")
target_folder_path = input("Target folder name: C:\\Users\\taigb\\")
starts_with = input("Starts with?: ")
ends_with = input("File format?: ")

source_path = fr"C:\Users\taigb\{source_folder_path}"

target_path = fr"C:\Users\taigb\{target_folder_path}"


def move():

    if not os.path.exists(target_path):
        os.makedirs(target_path)
        print()
        print("\n==========================================================================================")
        print(f"Folder '{target_folder_path}' was created successfully!")
        print("==========================================================================================\n")
    else:
        print("\n==========================================================================================")
        print(f"There's already a folder with path '{target_folder_path}'.")
        print("==========================================================================================\n")

    for file_name in os.listdir(source_path):

        if not file_name.lower().endswith(f"{ends_with}") and file_name.startswith(f"{starts_with}"):
            continue

        if file_name.lower().endswith(f"{ends_with}") and file_name.startswith(f"{starts_with}"):
            old_path = os.path.join(source_path, file_name)
            new_path = os.path.join(target_path, file_name)

            shutil.move(old_path, new_path)
            print(f"File {file_name} has been moved to folder {target_path} successfully!\n")

    print("==========================================================================================")


if __name__ == "__main__":
    move()
