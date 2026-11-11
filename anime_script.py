import os
import shutil
import re

source_path = r"C:\Users\EFEZINO\Downloads"
target_base_path = r"D:\Users\Videos\Series\Anime"


def extract_anime_info(file_name):
    """
    Extracts the anime title and season number from the filename.
    Examples:
      'AnimePahe_Sankarea_-_01_BD_1080p_Doki.mp4'               -> ('Sankarea', None)
      'AnimePahe_Kaiju_No._8_Season_2_-_01_1080p_SubsPlease.mp4' -> ('Kaiju No. 8', 2)
      'AnimePahe_Grand_Blue_-_S2E01_1080p.mp4'                  -> ('Grand Blue', 2)
      'Dandadan-S2E1-1080P.mp4'                                 -> ('Dandadan', 2)
      'Dandadan S2_S02E01_en.srt'                               -> ('Dandadan', 2)
    """
    base_name = os.path.splitext(file_name)[0]
    name = re.sub(r'^(?:AnimePahe_|\[.*?\]\s*)', '', base_name)

    season_num = None

    # Check for S02E01, -S2E1, etc.
    s_match = re.search(r'[-_. ]+S(?P<season>\d+)E\d+', name, re.IGNORECASE)
    if s_match:
        season_num = int(s_match.group('season'))
        name = name[:s_match.start()]
    elif '_-_' in name:
        name = name.split('_-_')[0]
    else:
        # Fallback regex for episode marker (e.g. _01_1080p, - 01)
        match = re.search(r'_\d{2,4}_(?:BD_)?(?:\d{3,4}p)|_\d{2,4}\.|\s+-\s+\d+', name)
        if match:
            name = name[:match.start()]
        else:
            name = re.sub(r'_\d{3,4}p.*$', '', name)

    # Check for season indicator in the title itself (e.g. Season 2, 2nd Season, S2)
    s_title = re.search(r'[-_. ]+(?:(?P<s1>\d+)(?:nd|rd|th)?_?Season|Season_?(?P<s2>\d+)|S(?P<s3>\d+))\b', name, re.IGNORECASE)
    if s_title:
        val = s_title.group('s1') or s_title.group('s2') or s_title.group('s3')
        if val:
            season_num = int(val)
        name = name[:s_title.start()]

    # Clean bracketed tags, replace underscores, and trim
    clean_name = re.sub(r'\[.*?\]|\(.*?\)', '', name).replace('_', ' ').strip()
    return clean_name, season_num


def get_target_folder(file_name):
    clean_name, season_num = extract_anime_info(file_name)

    # If season is > 1 and not already in clean_name, form candidate folder name
    if season_num and season_num > 1:
        if not re.search(rf'\b(?:S|Season\s*)?0*{season_num}\b$', clean_name, re.IGNORECASE):
            folder_candidate = f"{clean_name} S{season_num}"
        else:
            folder_candidate = clean_name
    else:
        folder_candidate = clean_name

    # Check if the series base folder exists and already has an S2/S3 subfolder
    root_name = re.sub(r'\s+(?:S\d+|Season\s*\d+|\d+(?:nd|rd|th)\s*Season)$', '', folder_candidate, flags=re.IGNORECASE).strip()

    if os.path.exists(target_base_path):
        existing_folders = os.listdir(target_base_path)

        # 1. If season > 1, check if root folder exists and contains an S{season} subfolder (e.g. Kaiju No. 8/S2)
        if season_num and season_num > 1:
            for ef in existing_folders:
                if ef.lower() == root_name.lower():
                    root_path = os.path.join(target_base_path, ef)
                    if os.path.isdir(root_path):
                        for sub in os.listdir(root_path):
                            if sub.lower() in [f"s{season_num}", f"season {season_num}", str(season_num)]:
                                return os.path.join(root_path, sub), f"{ef}\\{sub}"

        # 2. Check if an exact folder exists for this candidate (e.g. Dandadan S2 or Hell's Paradise 2)
        for ef in existing_folders:
            if ef.lower() == folder_candidate.lower():
                return os.path.join(target_base_path, ef), ef

        # 3. Check if base folder exists and season is 1, and contains S1
        if season_num == 1:
            for ef in existing_folders:
                if ef.lower() == root_name.lower():
                    root_path = os.path.join(target_base_path, ef)
                    if os.path.isdir(root_path):
                        for sub in os.listdir(root_path):
                            if sub.lower() in ["s1", "season 1", "1"]:
                                return os.path.join(root_path, sub), f"{ef}\\{sub}"
                    return root_path, ef

    # Default fallback: create/use the folder_candidate in target_base_path
    return os.path.join(target_base_path, folder_candidate), folder_candidate


def is_anime_file(file_name, existing_anime_names):
    # Ignore incomplete browser downloads
    if file_name.lower().endswith((".crdownload", ".part", ".tmp")):
        return False

    # Supported video and subtitle formats
    if not file_name.lower().endswith((".mp4", ".mkv", ".srt", ".ass")):
        return False

    # 1. AnimePahe downloads
    if file_name.startswith("AnimePahe_"):
        return True

    # 2. Standard anime release group prefixes
    if re.match(r'^\[(?:SubsPlease|Erai-raws|Judas|HorribleSubs|ASW|NanDesuKa|Yameii|EMBER|Doki|Nep_Blanc|Bunny-Apocalypse|Foxtrot|hchcsen|Vodes)[^\]]*\]', file_name, re.IGNORECASE):
        return True

    # 3. Matches an existing anime show in library
    name_clean, _ = extract_anime_info(file_name)
    if name_clean and any(name_clean.lower() == existing.lower() for existing in existing_anime_names):
        return True

    return False


def move():
    print("=" * 80)
    print(" ANIME FILE MOVER (Automatic)")
    print(f" Source: {source_path}")
    print(f" Target Base: {target_base_path}")
    print("=" * 80)

    if not os.path.exists(target_base_path):
        os.makedirs(target_base_path, exist_ok=True)
        print(f"\nCreated base folder: '{target_base_path}'\n")

    # Get known anime library folders to help identify downloads
    existing_anime = []
    if os.path.exists(target_base_path):
        existing_anime = [d for d in os.listdir(target_base_path) if os.path.isdir(os.path.join(target_base_path, d))]

    moved_count = 0
    skipped_crdownload = 0

    all_files = sorted(os.listdir(source_path))

    for file_name in all_files:
        if file_name.lower().endswith((".crdownload", ".part", ".tmp")):
            if file_name.startswith("AnimePahe_"):
                skipped_crdownload += 1
            continue

        if not is_anime_file(file_name, existing_anime):
            continue

        target_folder_path, display_name = get_target_folder(file_name)

        if not os.path.exists(target_folder_path):
            os.makedirs(target_folder_path, exist_ok=True)
            print(f"\n[+] Created folder: '{display_name}'")

        old_path = os.path.join(source_path, file_name)
        new_path = os.path.join(target_folder_path, file_name)

        try:
            shutil.move(old_path, new_path)
            print(f" -> Moved: {file_name} -> {display_name}\\")
            moved_count += 1
        except Exception as e:
            print(f"[!] Error moving '{file_name}': {e}")

    print("\n" + "=" * 80)
    print(f"Finished! Successfully moved {moved_count} anime file(s).")
    if skipped_crdownload > 0:
        print(f"Note: Skipped {skipped_crdownload} in-progress download (.crdownload) file(s).")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    move()
