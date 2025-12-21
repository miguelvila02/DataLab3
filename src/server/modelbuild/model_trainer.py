import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle
from pathlib import Path
import warnings

warnings.filterwarnings("ignore")


class PremierLeagueModelTrainer:
    """Simplified trainer that only trains and saves the model."""

    def __init__(self, n_estimators=150, max_depth=12, random_state=42):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.random_state = random_state
        self.model = None
        self.feature_names = None

    def create_features(self, matches_df):
        """
        Create features for training.
        This should match the feature creation in ModelAnalysis.
        """
        # Sort by date
        if "date" in matches_df.columns:
            matches_df = matches_df.sort_values("date").reset_index(drop=True)
        else:
            matches_df = matches_df.reset_index(drop=True)

        features_list = []

        for i, row in matches_df.iterrows():
            try:
                features = self._create_single_match_features(i, row)
                features_list.append(features)
            except Exception as e:
                continue

        features_df = pd.DataFrame(features_list)
        return features_df

    def _create_single_match_features(self, idx, row):
        """Create features for a single match."""
        features = {}

        # Basic features
        features["possession_diff"] = row["home_possession"] - row["away_possession"]
        features["shots_diff"] = row["home_shots_on_target"] - row["away_shots_on_target"]
        features["corners_diff"] = row["home_corners"] - row["away_corners"]
        features["fouls_diff"] = row["home_fouls"] - row["away_fouls"]
        features["home_possession"] = row["home_possession"]
        features["away_possession"] = row["away_possession"]

        # Target variable
        if row["home_goals"] > row["away_goals"]:
            features["outcome"] = 0  # Home win
        elif row["home_goals"] < row["away_goals"]:
            features["outcome"] = 2  # Away win
        else:
            features["outcome"] = 1  # Draw

        return features

    def train(self, matches_df):
        """Train the model on the provided data."""
        print("Training Random Forest model...")

        # Create features
        features_df = self.create_features(matches_df)

        # Separate features and target
        X = features_df.drop("outcome", axis=1)
        y = features_df["outcome"]

        # Store feature names
        self.feature_names = X.columns.tolist()

        # Create and train model
        self.model = RandomForestClassifier(
            n_estimators=self.n_estimators,
            max_depth=self.max_depth,
            min_samples_split=20,
            min_samples_leaf=10,
            random_state=self.random_state,
            class_weight="balanced",
            n_jobs=-1,
        )

        self.model.fit(X, y)

        print(f"Model trained on {len(X)} samples with {len(self.feature_names)} features")

        return self.model

    def save_model(self, model_path="models/random_forest_model.pkl"):
        """Save the trained model."""
        # Create directory if it doesn't exist
        Path(model_path).parent.mkdir(parents=True, exist_ok=True)

        # Save model and feature names
        model_data = {
            "model": self.model,
            "feature_names": self.feature_names,
            "parameters": {
                "n_estimators": self.n_estimators,
                "max_depth": self.max_depth,
                "random_state": self.random_state,
            },
        }

        with open(model_path, "wb") as f:
            pickle.dump(model_data, f)

        print(f"Model saved to: {model_path}")
        return model_path

    def load_model(self, model_path="models/random_forest_model.pkl"):
        """Load a trained model."""
        with open(model_path, "rb") as f:
            model_data = pickle.load(f)

        self.model = model_data["model"]
        self.feature_names = model_data["feature_names"]

        print(f"Model loaded from: {model_path}")
        return self


def main():
    """Main function to train and save the model."""
    print("=" * 70)
    print("MODEL TRAINER - PREMIER LEAGUE PREDICTION")
    print("=" * 70)

    # Load data
    try:
        data_path = "data/premier_league_matches.csv"
        matches_df = pd.read_csv(data_path)
        print(f"Loaded {len(matches_df)} matches from {data_path}")
    except FileNotFoundError:
        print(f"Error: Data file not found at {data_path}")
        print("Please run data_fetcher.py first to fetch data.")
        return

    # Initialize trainer
    trainer = PremierLeagueModelTrainer(n_estimators=150, max_depth=12, random_state=42)

    # Train model
    model = trainer.train(matches_df)

    # Save model
    model_path = trainer.save_model("models/random_forest_model.pkl")

    print("\n" + "=" * 70)
    print("TRAINING COMPLETE")
    print("=" * 70)
    print(f"\nModel saved to: {model_path}")
    print(f"\nFor comprehensive analysis, run:")
    print("python model_analysis.ipynb")

    return trainer


if __name__ == "__main__":
    trainer = main()