import os
import shutil
import re

source_path = r"C:\Users\EFEZINO\Downloads"
target_base_path = r"D:\Users\Videos\Series\K drama"


def extract_kdrama_name(file_name):
    """
    Extracts a clean K-drama series title and folder name from file names.
    Examples:
      'Behind Your Touch [English]-S1E1-480P.mp4' -> 'Behind Your Touch'
      'Behind Your Touch [English]_S01E01_en.srt' -> 'Behind Your Touch'
      'Welcome to Waikiki-S2E1-480P.mp4'          -> 'Welcome to Waikiki S2'
      'Welcome to Waikiki S2_S02E01_en.srt'       -> 'Welcome to Waikiki S2'
    """
    base_name = os.path.splitext(file_name)[0]

    # Look for season and episode pattern
    # Matches patterns like -S1E1, _S02E01, -S2E1, -E01, .S01E01, etc.
    pattern = r'[-_. ]+(?:S(?P<season>\d+))?E(?:pisode|p)?\s*\d+'
    match = re.search(pattern, base_name, re.IGNORECASE)

    season_num = None
    if match:
        name = base_name[:match.start()]
        if match.group('season'):
            season_num = int(match.group('season'))
    else:
        # Fallback: cut before resolution/codec tags if present
        res_match = re.search(r'[-_. ]+(?:\d{3,4}p|HD|FHD|WEB-?DL)', base_name, re.IGNORECASE)
        if res_match:
            name = base_name[:res_match.start()]
        else:
            name = base_name

    # Remove bracketed language or release tags like [English], [Eng Sub], (K-Drama), etc.
    name = re.sub(r'\[.*?\]|\(.*?\)', '', name)

    # Clean up formatting
    name = name.replace("_", " ").strip()

    # If Season is 2 or higher (e.g. S2, S3), ensure the folder name includes the season
    if season_num and season_num > 1:
        # Check if the name already ends with S2, Season 2, or the season number
        if not re.search(rf'\b(?:S|Season\s*)?0*{season_num}\b$', name, re.IGNORECASE):
            name = f"{name} S{season_num}"

    return name


def move():
    print("=" * 80)
    print(" K-DRAMA FILE MOVER (Automatic)")
    print(f" Source: {source_path}")
    print(f" Target Base: {target_base_path}")
    print("=" * 80)

    if not os.path.exists(target_base_path):
        os.makedirs(target_base_path, exist_ok=True)
        print(f"\nCreated base folder: '{target_base_path}'\n")

    moved_count = 0
    skipped_crdownload = 0

    all_files = sorted(os.listdir(source_path))

    for file_name in all_files:
        # Ignore incomplete browser downloads (.crdownload, .part, .tmp)
        if file_name.lower().endswith((".crdownload", ".part", ".tmp")):
            skipped_crdownload += 1
            continue

        # Only process .mp4 and .srt files
        if not file_name.lower().endswith((".mp4", ".srt")):
            continue

        # Check if this file has season/episode pattern indicating a series episode
        if not re.search(r'(?:S\d+)?E(?:pisode|p)?\s*\d+', file_name, re.IGNORECASE):
            continue

        folder_title = extract_kdrama_name(file_name)
        if not folder_title:
            continue

        target_folder = os.path.join(target_base_path, folder_title)
        if not os.path.exists(target_folder):
            os.makedirs(target_folder, exist_ok=True)
            print(f"\n[+] Created folder: '{target_folder}'")

        old_path = os.path.join(source_path, file_name)
        new_path = os.path.join(target_folder, file_name)

        try:
            shutil.move(old_path, new_path)
            print(f" -> Moved: {file_name} -> {folder_title}\\")
            moved_count += 1
        except Exception as e:
            print(f"[!] Error moving '{file_name}': {e}")

    print("\n" + "=" * 80)
    print(f"Finished! Successfully moved {moved_count} file(s).")
    if skipped_crdownload > 0:
        print(f"Note: Skipped {skipped_crdownload} in-progress download (.crdownload) file(s).")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    move()
