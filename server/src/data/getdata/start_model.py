import sqlite3
import os
import pandas as pd
import kagglehub
import json
import subprocess
from pathlib import Path
from datetime import datetime

path = kagglehub.dataset_download("hugomathien/soccer")

conn = sqlite3.connect(os.path.join(path, 'database.sqlite'))


def premier_league_matches(connection):
    query = (
        "Select home_team_goal, away_team_goal, possession, shoton, corner, "
        "foulcommit\n"
        "From Match\n"
        "Join League On Match.league_id = 1729"
    )
    df = pd.read_sql_query(query, connection)
    return df


def save_matches(df, filepath):
    df.to_csv(filepath, index=False)


def dvc_push(matches_df, metadata=None):
    subprocess.run(["dvc", "add", "server/src/data/raw_data.csv"])
    subprocess.run(["git", "add", "server/src/data/raw_data.csv.dvc"])
    subprocess.run(['git', 'add', 'server/src/data/.gitignore'], check=True)
    commit_message = f"Data update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    subprocess.run(["git", "commit", "-m", commit_message])
    subprocess.run(["dvc", "remote", "add", "-f", "myremote", "s3://mybucket/dvcstore"])
    subprocess.run(["dvc", "push", "-r", "myremote"])
    subprocess.run(["git", "add", "server/src/data/data_metadata.json"])
    subprocess.run(["git", "commit", "-m", "Update data metadata"])
    subprocess.run(["git", "push"]) 
    
    if metadata is None:
        metadata = {}

    metadata.update({
        "last_updated": datetime.now().isoformat(),
        "data_file": "raw_data.csv",
        "dataframe_shape": matches_df.shape,
        "columns": matches_df.columns.tolist(),
        "row_count": len(matches_df)
    })

    with open("server/src/data/data_metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)


if __name__ == "__main__":
    matches_df = premier_league_matches(conn)
    save_path = Path(__file__).resolve().parent.parent / "raw_data.csv"
    save_matches(matches_df, save_path)
    dvc_push(matches_df)
    print("\n\nData extraction completed.")
    print("Starting data filtering and preprocessing...\n")

