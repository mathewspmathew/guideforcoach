import pandas as pd
import joblib
import os
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors
from src.config import FEATURES, MODEL_PATH, SCALER_PATH, DB_PATH, N_NEIGHBORS, METRIC

class SimilarityEngine:
    def __init__(self):
        self.model = NearestNeighbors(n_neighbors=N_NEIGHBORS, metric=METRIC)
        self.scaler = MinMaxScaler()
        self.df = None # Holds the reference database

    def train(self, df: pd.DataFrame):
        """
        Trains the KNN model and saves artifacts.
        """
        self.df = df

        # 1. Extract Feature Matrix
        X = df[FEATURES].values

        # 2. Scale Data (0-1)
        X_scaled = self.scaler.fit_transform(X)

        # 3. Fit Model
        self.model.fit(X_scaled)

        # 4. Save Artifacts (MLOps)
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        joblib.dump(self.model, MODEL_PATH)
        joblib.dump(self.scaler, SCALER_PATH)
        joblib.dump(self.df, DB_PATH)
        print("✅ Model trained and saved successfully.")

    def inference(self, player_name: str):
        """
        Loads the model and finds similar players.
        """
        # return (DB_PATH)
        # Lazy Loading: Only load if not in memory
        if self.df is None:
            if not os.path.exists(DB_PATH):
                return {"error": "Model not trained yet."}
            self.df = joblib.load(DB_PATH)
            self.model = joblib.load(MODEL_PATH)
            self.scaler = joblib.load(SCALER_PATH)

        # 1. Find the Target Player
        # Case-insensitive partial match
        matches = self.df[self.df['Player'].str.contains(player_name, case=False, na=False)]

        if matches.empty:
            return {"error": f"Player '{player_name}' not found."}

        # Pick the first match
        target_idx = matches.index[0]
        target_data = self.df.loc[target_idx]

        # 2. Prepare Vector
        vector = target_data[FEATURES].values.reshape(1, -1)
        vector_scaled = self.scaler.transform(vector)

        # 3. Find Neighbors
        distances, indices = self.model.kneighbors(vector_scaled)

        # 4. Format Output
        results = []
        # Loop through neighbors (Skip index 0 as it's the player themselves)
        for i in range(1, len(indices[0])):
            idx = indices[0][i]
            dist = distances[0][i]

            player_info = self.df.loc[idx]

            # Simple similarity score (Euclidean distance -> %)
            # A distance of 0 is 100% match. A distance of 1.0 is ~0% match.
            score = max(0, (1 - dist) * 100)

            results.append({
                "name": player_info['Player'],
                "squad": player_info['Squad'],
                "age": int(player_info['Age']),
                "similarity": round(score, 1)
            })

        # only for debug
        # print({"target": target_data['Player'],
        #     "target_squad": target_data['Squad'],
        #     "recommendations": results})

        return {
            "target": target_data['Player'],
            "target_squad": target_data['Squad'],
            "recommendations": results
        }

#only for debugging
# if __name__ == "__main__":
#     test = SimilarityEngine()
#     test.inference("Matthis Abline")