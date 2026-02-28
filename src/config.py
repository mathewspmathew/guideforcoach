# import os
from pathlib import Path

DATA_DIR = Path("data")
MODEL_DIR = Path("models")

MODEL_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

RAW_DATA_PATH = DATA_DIR/ "players_data_light-2024_2025.csv"
MODEL_PATH = MODEL_DIR/ "knn_model.pkl"
SCALER_PATH = MODEL_DIR/ "scaler.pkl"
DB_PATH = MODEL_DIR/ "player_database.pkl" #for cleaned data

# for neighbors
N_NEIGHBORS = 5
METRIC = 'euclidean' #'cosine' is also good, but euclidean works well for magnitude

# The raw columns we need from the CSV to calculate the final stats
REQUIRED_COLS = [
    'Player', 'Nation', 'Pos', 'Squad', 'Age', '90s',
    'npxG', 'xAG', 'PrgP', 'PrgC', 'TklW', 'Int', 'Recov', 'KP'
]

# The final calculated features (Per 90) that go into the ML Model
FEATURES = [
    'npxG_p90',   # Finishing
    'xAG_p90',    # Assisting
    'PrgP_p90',   # Passing Progression
    'PrgC_p90',   # Dribbling Progression
    'TklW_p90',   # Tackling
    'Int_p90',    # Reading the game
    'Recov_p90',  # Work rate
    'KP_p90'      # Creativity
]