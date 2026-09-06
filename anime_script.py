import os
import shutil
import re

source_path = r"C:\Users\taigb\Downloads"
target_base_path = r"C:\Users\taigb\Videos\Series\Anime"

def extract_anime_name(file_name):
    # Remove the prefix
    name = file_name.replace("AnimePahe_", "")
    
    # Try to split by "_-_" which is the most common AnimePahe delimiter
    if "_-_" in name:
        name = name.split("_-_")[0]
    else:
        # Regex explanation:
        # Looks for an episode number (e.g., _01_, _12_) followed by optional tags like BD, and a resolution (720p, 1080p, etc.)
        # Or looks for an episode number just before the extension
        match = re.search(r'_\d{2,4}_(?:BD_)?(?:\d{3,4}p)|_\d{2,4}\.', name)
        if match:
            name = name[:match.start()]
        else:
            # Fallback if no episode pattern is clearly found, strip resolution and extension
            name = re.sub(r'_\d{3,4}p.*$', '', name)
            name = name.rsplit('.', 1)[0]
    
    return name.replace("_", " ").strip()

def move():
    if not os.path.exists(target_base_path):
        os.makedirs(target_base_path)
        print(f"\n==========================================================================================")
        print(f"Base folder '{target_base_path}' was created successfully!")
        print(f"==========================================================================================\n")

    moved_count = 0
    for file_name in os.listdir(source_path):
        if file_name.startswith("AnimePahe_") and file_name.lower().endswith((".mp4", ".mkv")):
            anime_name = extract_anime_name(file_name)
            target_folder_path = os.path.join(target_base_path, anime_name)
            
            if not os.path.exists(target_folder_path):
                os.makedirs(target_folder_path)
                print(f"\n==========================================================================================")
                print(f"Folder '{anime_name}' was created successfully!")
                print(f"==========================================================================================\n")
            
            old_path = os.path.join(source_path, file_name)
            new_path = os.path.join(target_folder_path, file_name)
            
            try:
                shutil.move(old_path, new_path)
                print(f"File {file_name} has been moved to folder {target_folder_path} successfully!\n")
                moved_count += 1
            except Exception as e:
                print(f"Error moving {file_name}: {e}\n")

    if moved_count > 0:
        print("==========================================================================================")
        print(f"Finished moving {moved_count} anime files.")
        print("==========================================================================================\n")

if __name__ == "__main__":
    move()
