"""
Player name validation against the local dataset.

Loads the player CSV once at import time and builds a fast lowercase lookup set.
Incoming names are matched case-insensitively so "lionel messi" == "Lionel Messi".
if the CSV is missing — validation is skipped in that case.
"""

from pathlib import Path
import pandas as pd
import warnings

_DATA_PATH = (
    Path(__file__).resolve().parents[1] / "data" / "players_data_light-2024_2025.csv"
)

_KNOWN_PLAYERS: set[str] = set()

try:
    _df = pd.read_csv(_DATA_PATH, usecols=["Player"])
    _KNOWN_PLAYERS = {name.strip().lower() for name in _df["Player"].dropna()}
except Exception as exc:
    warnings.warn(f"Could not load player list for validation: {exc}")


def is_known_player(player_name: str) -> bool:
    """Return True if the name matches a player in the dataset."""
    if not _KNOWN_PLAYERS:
        return True  # CSV unavailable — let the request through
    return player_name.strip().lower() in _KNOWN_PLAYERS


def known_player_count() -> int:
    """Return the number of unique players loaded for validation."""
    return len(_KNOWN_PLAYERS)
