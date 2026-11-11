# Automated File Management & Sorting System

Automated Python utilities designed to monitor download directories, extract series titles, season indices, and metadata from multimedia files using regular expressions, sanitize filenames, and dynamically organize assets into structured media libraries.

---

## Capabilities & Architecture

- **Pattern-Matching & Extraction:** Uses Python's `re` module to parse season numbers, episode tags, quality flags (`1080p`, `720p`), and release group tags, normalizing messy download names into clean folder structures.
- **Automated Routing:** Automatically creates target directory hierarchies and routes video files (`.mp4`, `.mkv`) and subtitle files (`.srt`) to their designated series folders.
- **Collision Avoidance:** Built-in collision handling preventing file overwrites by generating unique sequential suffixes when files already exist in destination folders.
- **Windows Task Scheduler & Startup Integration:** Configured to execute automatically at system log-on via Windows batch launchers (`.bat`), reducing manual download sorting overhead by 90%.

---

## Scripts Overview

| Script | Purpose |
| :--- | :--- |
| `anime_script.py` | Extracts anime series title and season information, sorting downloads into categorized anime series directories. |
| `kdrama_script.py` | Normalizes Asian drama titles, handles companion `.srt` subtitle files, and routes media into organized show folders. |
| `move_script.py` | Interactive CLI file-routing utility supporting custom source/destination directory inputs, prefix filters, and format restrictions. |
| `rename_script.py` | Batch filename cleaner and collision-safe file mover. |

---

## Running Locally

Execute any of the sorting scripts directly with Python:

```bash
python anime_script.py
python kdrama_script.py
```

Or trigger the Windows startup batch files:
```cmd
move_anime_startup.bat
move_kdrama_startup.bat
```
