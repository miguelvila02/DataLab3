import pandas as pd
from typing import Tuple
import subprocess
import json
from random import randint
from datetime import datetime


def generate_possession(
        home_goals: int, away_goals: int
        ) -> Tuple[float, float]:
    """Generate possession percentages based on goals scored."""
    goal_diff = home_goals - away_goals
    base_possession = 50.0
    if goal_diff > 2:
        possession_shift = randint(15, 25)
    elif 0 < goal_diff <= 2:
        possession_shift = randint(0, 15)
    elif -2 <= goal_diff < 0:
        possession_shift = -randint(0, 15)
    else:
        possession_shift = -randint(15, 25)
    home_poss = base_possession + possession_shift
    away_poss = 100.0 - home_poss
    return home_poss, away_poss


def generate_shots_on_target(
        home_goals: int, away_goals: int,
        home_poss: int, away_poss: int
        ) -> Tuple[int, int]:
    """Generate shots on target based on goals scored."""
    possession_diff = home_poss - away_poss
    if possession_diff > 20:
        if home_goals == 0:
            home_shots = randint(5, 10)
        else:
            home_shots = home_goals * randint(2, 4)
        if away_goals == 0:
            away_shots = randint(1, 2)
        else:
            away_shots = away_goals * 1 + randint(0, 2)
    elif 0 < possession_diff <= 20:
        if home_goals == 0:
            home_shots = randint(3, 6)
        else:
            home_shots = home_goals * 3 + randint(0, 4)
        if away_goals == 0:
            away_shots = randint(2, 4)
        else:
            away_shots = away_goals * 2 + randint(0, 2)
    elif -20 <= possession_diff < 0:
        if home_goals == 0:
            home_shots = randint(2, 5)
        else:
            home_shots = home_goals * 2 + randint(0, 3)
        if away_goals == 0:
            away_shots = randint(3, 5)
        else:
            away_shots = away_goals * 3 + randint(0, 2)
    else:
        if home_goals == 0:
            home_shots = randint(1, 3)
        else:
            home_shots = home_goals * 1 + randint(0, 3)
        if away_goals == 0:
            away_shots = randint(4, 8)
        else:
            away_shots = away_goals * randint(2, 4)

    return home_shots, away_shots


def generate_corners(
        home_shots: int, away_shots: int
        ) -> Tuple[int, int]:
    """Generate corner kicks based on shots on target."""
    home_corners = home_shots // randint(1, 2) + randint(0, 3)
    away_corners = away_shots // randint(1, 3) + randint(0, 2)
    return home_corners, away_corners


def generate_fouls(
        home_poss: float, away_poss: float
        ) -> Tuple[int, int]:
    """Generate fouls committed based on possession percentages."""
    foul_average = 22
    home_fouls = int(foul_average * (away_poss / 100)) + randint(-5, 5)
    away_fouls = int(foul_average * (home_poss / 100)) + randint(-5, 5)
    return home_fouls, away_fouls


def update_game_stats(
        csv_file: str = 'server/src/data/raw_data.csv'
        ) -> pd.DataFrame:
    """Update game statistics to a new dataset."""
    updates_made = 0

    df = pd.read_csv(csv_file)
    updated_data = []
    for _, row in df.iterrows():
        home_goals = row['home_team_goal']
        away_goals = row['away_team_goal']
        home_poss, away_poss = generate_possession(home_goals, away_goals)
        updates_made += 2
        home_shots, away_shots = generate_shots_on_target(
            home_goals, away_goals, home_poss, away_poss
        )
        updates_made += 2
        home_corners, away_corners = generate_corners(home_shots, away_shots)
        updates_made += 2
        home_fouls, away_fouls = generate_fouls(home_poss, away_poss)
        updates_made += 2

        updated_data.append({
            'home_team_goal': home_goals,
            'away_team_goal': away_goals,
            'possession_home': home_poss,
            'possession_away': away_poss,
            'shoton_home': home_shots,
            'shoton_away': away_shots,
            'corner_home': home_corners,
            'corner_away': away_corners,
            'foulcommit_home': home_fouls,
            'foulcommit_away': away_fouls
        })
    updated_df = pd.DataFrame(updated_data)
    updated_df.to_csv('server/src/data/processed_data.csv', index=False)


def dvc_push(updated_df, metadata=None):
    subprocess.run(["dvc", "add", "server/src/data/processed_data.csv"])
    subprocess.run(["git", "add", "server/src/data/processed_data.csv.dvc"])
    subprocess.run(['git', 'add', 'server/src/data/.gitignore'], check=True)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    commit_message = f"Processed data update: {timestamp}"
    subprocess.run(["git", "commit", "-m", commit_message])
    subprocess.run([
        "dvc", "remote", "add", "-f",
        "myremote", "s3://mybucket/dvcstore"
    ])
    subprocess.run(["dvc", "push", "-r", "myremote"])
    subprocess.run(["git", "add", "server/src/data/data_metadata.json"])
    subprocess.run(["git", "commit", "-m", "Update processed data metadata"])
    subprocess.run(["git", "push"])

    if metadata is None:
        metadata = {}

    metadata.update({
        "last_updated": datetime.now().isoformat(),
        "data_file": "processed_data.csv",
        "dataframe_shape": updated_df.shape,
        "columns": updated_df.columns.tolist(),
        "row_count": len(updated_df)
    })

    with open("server/src/data/data_metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)


if __name__ == "__main__":
    updated_df = update_game_stats()
    dvc_push(updated_df, metadata=None)
