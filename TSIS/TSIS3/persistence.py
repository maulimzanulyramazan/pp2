import json  # Module for JSON (JavaScript Object Notation) file handling (parse and write)
from pathlib import Path  # Object-oriented filesystem path handling (better than os.path)

SETTINGS_FILE = Path("settings.json")  # Define file path for storing game settings
LEADERBOARD_FILE = Path("leaderboard.json")  # Define file path for storing high scores

DEFAULT_SETTINGS = {  # Default configuration values if settings file doesn't exist
    "sound": True,  # Master sound on/off (boolean)
    "car_color": "red",  # Player's car color choice (string)
    "difficulty": "normal",  # Game difficulty level (normal, hard, etc.)
    "music_volume": 20  # Music volume level (0-100 integer)
}

def load_settings():
    if not SETTINGS_FILE.exists():  # Check if settings file exists on disk
        save_settings(DEFAULT_SETTINGS)  # Create file with default settings
        return DEFAULT_SETTINGS.copy()  # Return copy of defaults (not original dict)

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:  # Open file for reading with UTF-8 encoding
            data = json.load(file)  # Parse JSON content into Python dictionary
            return {**DEFAULT_SETTINGS, **data}  # Merge: defaults first, then user settings override
    except json.JSONDecodeError:  # Handle corrupted/invalid JSON file
        return DEFAULT_SETTINGS.copy()  # Return defaults if JSON parsing fails

def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:  # Open file for writing (creates/overwrites)
        json.dump(settings, file, indent=4)  # Write settings as JSON with 4-space indentation for readability

def load_leaderboard():
    if not LEADERBOARD_FILE.exists():  # Check if leaderboard file exists
        save_leaderboard([])  # Create empty leaderboard file with empty list
        return []  # Return empty list (no scores yet)

    try:
        with open(LEADERBOARD_FILE, "r", encoding="utf-8") as file:  # Open leaderboard for reading
            return json.load(file)  # Parse and return list of score entries
    except json.JSONDecodeError:  # Handle corrupted leaderboard file
        return []  # Return empty list as fallback

def save_leaderboard(scores):
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as file:  # Open leaderboard for writing
        json.dump(scores, file, indent=4)  # Write scores as JSON with 4-space indentation

def add_score(name, score, distance, coins):
    scores = load_leaderboard()  # Get current list of high scores
    scores.append({  # Add new score entry as dictionary
        "name": name,  # Player's username (string)
        "score": int(score),  # Total score (converted to int)
        "distance": int(distance),  # Distance traveled (converted to int)
        "coins": int(coins)  # Number of coins collected (converted to int)
    })
    scores.sort(key=lambda item: item["score"], reverse=True)  # Sort descending by score (highest first)
    save_leaderboard(scores[:10])  # Keep only top 10 scores, discard the rest