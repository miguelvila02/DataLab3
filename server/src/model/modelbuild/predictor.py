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


def joblib_to_dvc(model_path: Path):
    import subprocess
    subprocess.run(["dvc", "add", str(model_path)])
    subprocess.run(["git", "add", f"{model_path}.dvc"])
    subprocess.run(['git', 'add', 'server/src/model/.gitignore'], check=True)
    commit_message = f"Model update: {model_path.name}"
    subprocess.run(["git", "commit", "-m", commit_message])
    subprocess.run([
        "dvc", "remote", "add", "-f",
        "myremote", "s3://mybucket/dvcstore"
    ])
    subprocess.run(["dvc", "push", "-r", "myremote"])
    subprocess.run(["git", "push"])


if __name__ == "__main__":
    model_path = Path('server/src/model/match_predictor.joblib')
    save_model(model, model_path)
    joblib_to_dvc(model_path)
    print("\nYou are good to go!")
