import os
import shutil
import re

source_path = r"C:\Users\taigb\Downloads"

def get_unique_filename(target_folder, base_name, extension):
    """
    Finds the next available filename in the target folder to prevent collisions.
    It checks for base_name.extension, base_name (1).extension, etc.
    """
    # First check if the exact base name is available
    if not os.path.exists(os.path.join(target_folder, f"{base_name}{extension}")):
        return f"{base_name}{extension}"
    
    # If not, increment a counter until we find a free name
    counter = 1
    while True:
        new_name = f"{base_name} ({counter}){extension}"
        if not os.path.exists(os.path.join(target_folder, new_name)):
            return new_name
        counter += 1

def move_and_rename_videos():
    print("This script will find downloaded files with a specific name,")
    print("rename them correctly to avoid duplicate '(1)' issues, and move them.\n")
    
    search_name = input("Enter the base name of the files as downloaded (e.g., 'video'): ").strip()
    if not search_name:
        print("No name entered. Exiting.")
        return
        
    target_folder = input(r"Enter the target folder path (e.g., C:\Users\taigb\Videos\Series\MySeries): ").strip()
    if not target_folder:
        print("No target folder entered. Exiting.")
        return
        
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
        print(f"Created target folder: {target_folder}")

    moved_count = 0
    for file_name in os.listdir(source_path):
        # Check if the file starts with the search name and is a video file (or any file, really)
        if file_name.startswith(search_name) and os.path.isfile(os.path.join(source_path, file_name)):
            
            # We want to extract the true base name, ignoring browser-added " (1)", " (2)" etc.
            name_without_ext, extension = os.path.splitext(file_name)
            
            # Remove browser enumerator like " (1)" from the end of the name if it exists
            # This regex matches " (digits)" at the end of the string
            clean_base_name = re.sub(r'\s*\(\d+\)$', '', name_without_ext).strip()
            
            # Ensure it actually matches the search name after cleaning (in case they typed "video" but file is "video_other")
            if clean_base_name == search_name or clean_base_name.startswith(search_name):
                
                # Get a unique name in the target folder
                new_file_name = get_unique_filename(target_folder, clean_base_name, extension)
                
                old_path = os.path.join(source_path, file_name)
                new_path = os.path.join(target_folder, new_file_name)
                
                try:
                    shutil.move(old_path, new_path)
                    print(f"Moved and renamed: '{file_name}' -> '{new_file_name}'")
                    moved_count += 1
                except Exception as e:
                    print(f"Failed to move '{file_name}': {e}")

    print(f"\nFinished. Successfully moved and renamed {moved_count} file(s).")

if __name__ == "__main__":
    move_and_rename_videos()