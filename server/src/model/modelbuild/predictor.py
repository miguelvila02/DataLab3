import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


dataset_path = Path('server/src/data/processed_data.csv')
dataset = pd.read_csv(dataset_path)
X: pd.DataFrame = dataset.drop(
    columns=['home_team_goal', 'away_team_goal']
)
Y: pd.Series = np.where(
    dataset['home_team_goal'] > dataset['away_team_goal'], 1,
    np.where(
        dataset['home_team_goal'] < dataset['away_team_goal'], -1,
        0
    )
)
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.2, random_state=42
)
model = RandomForestClassifier(n_estimators=200, random_state=42)

model.fit(X_train, Y_train)

Y_pred = model.predict(X_test)


def predict_match(features: pd.DataFrame) -> np.ndarray:
    return model.predict(features)


def predict_proba(features: pd.DataFrame) -> np.ndarray:
    return model.predict_proba(features)


def save_model(model, filepath: Path):
    import joblib
    joblib.dump(model, filepath)


if __name__ == "__main__":
    model_path = Path('server/src/model/premier_league_model.joblib')
    save_model(model, model_path)
    print(f"Model saved to {model_path}")
