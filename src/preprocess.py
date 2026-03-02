import pandas as pd
import numpy as np
from src.config import RAW_DATA_PATH, REQUIRED_COLS

# print(REQUIRED_COLS)

class DataPreprocessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    def load_clean_data(self):
        """
        Loads CSV, filters GKs, removes players with low minutes,
        and calculates per-90 stats.
        """
        try:
            # Load only necessary columns to save memory
            df = pd.read_csv(self.file_path, usecols=lambda x: x in REQUIRED_COLS or x in ['Player', 'Squad', 'Pos', '90s'])

            # 1. Filter: Remove Goalkeepers and Low Minutes
            df = df[df['Pos'] != 'GK']
            df = df[df['90s'] >= 5.0].copy() # Must have played at least 5 games

            # 2. Feature Engineering: Calculate Per 90 Stats
            # Using .loc to avoid SettingWithCopy warnings
            df['npxG_p90'] = df['npxG'] / df['90s']
            df['xAG_p90'] = df['xAG'] / df['90s']
            df['PrgP_p90'] = df['PrgP'] / df['90s']
            df['PrgC_p90'] = df['PrgC'] / df['90s']
            df['TklW_p90'] = df['TklW'] / df['90s']
            df['Int_p90'] = df['Int'] / df['90s']
            df['Recov_p90'] = df['Recov'] / df['90s']
            df['KP_p90'] = df['KP'] / df['90s']

            # 3. Cleanup: Fill NaNs with 0
            # df.fillna(0, inplace=True)

            self.df = df.reset_index(drop=True)
            print(f"✅ Data Processed. Active Players: {len(self.df)}")
            return self.df

        except FileNotFoundError:
            raise FileNotFoundError(f"❌ Could not find file at {self.file_path}")

# if __name__ == "__main__":
#     preprocessor = DataPreprocessor(RAW_DATA_PATH)
#     df_clean = preprocessor.load_clean_data()
# only for testing