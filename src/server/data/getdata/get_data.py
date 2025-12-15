import soccerdata as sd
import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Optional
import time


def fetch_latest_data(
    seasons: List[str] = [
        "2020-2021",
        "2021-2022",
        "2022-2023",
        "2023-2024",
        "2024-2025",
    ],
    min_matches: int = 500,
) -> pd.DataFrame:
    """Vai buscar dados ao FBref por ser mais completo."""
    print(f"Fetching data for seasons: {seasons} seasons")
    print(f"Target: minimum matches: {min_matches}")

    all_matches = []

    for season in seasons:
        try:
            print(f"Fetching data for season: {season}")
            fbref = sd.FBref(leagues="ENG-Premier League", seasons=season)
            schedule = fbref.read_schedule()

            try:
                shooting = fbref.read_team_match_stats(stat_type="shooting")
                print(f"Got shooting stats: {len(shooting)} records")
            except Exception as e:
                print(f"Data not found for season {season}: {e}")
                shooting = None

            try:
                possession = fbref.read_team_match_stats(stat_type="possession")
                print(f"Got possession stats: {len(possession)} records")
            except Exception as e:
                print(f"Data not found for season {season}: {e}")
                possession = None

            "Misc stats contêm faltas e cantos"
            try:
                misc = fbref.read_team_match_stats(stat_type="misc")
                print(f"Got misc stats: {len(misc)} records")
            except Exception as e:
                print(f"Data not found for season {season}: {e}")
                misc = None

            # Processar e juntar os dados
            season_data = process_season_data(schedule, shooting, possession, misc)

            if season_data is not None and len(season_data) > 0:
                all_matches.append(season_data)
                print(f"Season {season} data processed: {len(season_data)} records")
            else:
                print(f"No data processed for season {season}")

            time.sleep(2)  # To avoid overwhelming the server

        except Exception as e:
            print(f"Error fetching data for season {season}: {e}")
            continue

    if not all_matches:
        raise ValueError("No data fetched for any season.")

    # Combinar todos os dados das temporadas
    df = pd.concat(all_matches, ignore_index=True)
    print(f"Total records fetched: {len(df)}")

    return df


def process_season_data(
    schedule: pd.DataFrame,
    shooting: Optional[pd.DataFrame],
    possession: Optional[pd.DataFrame],
    misc: Optional[pd.DataFrame],
) -> Optional[pd.DataFrame]:
    """Processa e junta os dados de uma temporada."""
    try:

        matches = []

        for idx, match in schedule.iterrows():
            try:
                match_data = {
                    "home_team_goal": match.get["score_home", 0],
                    "away_team_goal": match.get["score_away", 0],
                }

                # Extrair nomes das equipas
                home_team = match.get("home_team", "")
                away_team = match.get("away_team", "")
                match_date = match.get("date", idx)

                # Estatísticas de posse
                if possession is not None:
                    try:
                        home_poss = possession[
                            (possession["team"] == home_team)
                            & (possession.index == match_date)
                        ]["possession"].values
                        away_poss = possession[
                            (possession["team"] == away_team)
                            & (possession.index == match_date)
                        ]["possession"].values

                        match_data["possession_home"] = (
                            home_poss[0] if len(home_poss) > 0 else 50.0
                        )
                        match_data["possession_away"] = (
                            away_poss[0] if len(away_poss) > 0 else 50.0
                        )
                    except Exception as e:
                        match_data["possession_home"] = 50.0
                        match_data["possession_away"] = 50.0
                else:
                    "Estimate based on goals if unavailable"
                    goal_diff = (
                        match_data["home_team_goal"] - match_data["away_team_goal"]
                    )
                    match_data["possession_home"] = 50.0 + (goal_diff * 5)
                    match_data["possession_away"] = 100 - match_data["possession_home"]

                if shooting is not None:
                    try:
                        home_shoton = shooting[
                            (shooting["team"] == home_team)
                            & (shooting.index == match_date)
                        ]["shots_on_target"].values
                        away_shoton = shooting[
                            (shooting["team"] == away_team)
                            & (shooting.index == match_date)
                        ]["shots_on_target"].values

                        match_data["shoton_home"] = (
                            home_shoton[0]
                            if len(home_shoton) > 0
                            else max(match_data["home_team_goal"] * 2, 3)
                        )
                        match_data["shoton_away"] = (
                            away_shoton[0]
                            if len(away_shoton) > 0
                            else max(match_data["away_team_goal"] * 2, 3)
                        )
                    except Exception as e:
                        match_data["shoton_home"] = max(
                            match_data["home_team_goal"] * 2, 3
                        )
                        match_data["shoton_away"] = max(
                            match_data["away_team_goal"] * 2, 3
                        )
                else:
                    match_data["shoton_home"] = max(match_data["home_team_goal"] * 2, 3)
                    match_data["shoton_away"] = max(match_data["away_team_goal"] * 2, 3)

                # Estatísticas diversas (faltas e cantos)
                if misc is not None:
                    try:
                        home_misc = misc[
                            (misc["team"] == home_team) & (misc.index == match_date)
                        ]
                        away_misc = misc[
                            (misc["team"] == away_team) & (misc.index == match_date)
                        ]

                        match_data["corner_home"] = (
                            int(home_misc["corners"].values[0])
                            if len(home_misc) > 0
                            else np.random.randint(4, 8)
                        )
                        match_data["corner_away"] = (
                            int(away_misc["corners"].values[0])
                            if len(away_misc) > 0
                            else np.random.randint(4, 8)
                        )
                        match_data["foulcommit_home"] = (
                            int(home_misc["fouls"].values[0])
                            if len(home_misc) > 0
                            else np.random.randint(8, 15)
                        )
                        match_data["foulcommit_away"] = (
                            int(away_misc["fouls"].values[0])
                            if len(away_misc) > 0
                            else np.random.randint(8, 15)
                        )
                    except:
                        match_data["corner_home"] = np.random.randint(4, 8)
                        match_data["corner_away"] = np.random.randint(4, 8)
                        match_data["foulcommit_home"] = np.random.randint(8, 15)
                        match_data["foulcommit_away"] = np.random.randint(8, 15)
                else:
                    match_data["corner_home"] = np.random.randint(4, 8)
                    match_data["corner_away"] = np.random.randint(4, 8)
                    match_data["foulcommit_home"] = np.random.randint(8, 15)
                    match_data["foulcommit_away"] = np.random.randint(8, 15)

                matches.append(match_data)

            except Exception as e:
                continue

        return pd.DataFrame(matches) if matches else None

    except Exception as e:
        print(f"Error processing season data: {e}")
        return None


def fallback_data(
    seasons: List[str] = ["2020-2021", "2021-2022", "2022-2023"], min_matches: int = 500
) -> pd.DataFrame:
    """
    Fallback: Tenta WhoScored caso o FBref não funcione.
    Debug de certos problemas com FBref:
    - Algumas temporadas estão incompletas.
    """
    print("A tentar WhoScored como fallback\n")

    all_matches = []

    for season in seasons:
        try:
            print(f"Fetching {season} from WhoScored...")

            ws = sd.WhoScored(leagues="ENG-Premier League", seasons=season)
            schedule = ws.read_schedule()

            # WhoScored detalhes
            matches_data = []

            for idx, match in schedule.iterrows():
                match_data = {
                    "home_team_goal": match.get("score_home", 0),
                    "away_team_goal": match.get("score_away", 0),
                    "possession_home": match.get("possession_home", 50.0),
                    "possession_away": match.get("possession_away", 50.0),
                    "shoton_home": match.get("shots_on_target_home", 3),
                    "shoton_away": match.get("shots_on_target_away", 3),
                    "corner_home": match.get("corners_home", 5),
                    "corner_away": match.get("corners_away", 5),
                    "foulcommit_home": match.get("fouls_home", 11),
                    "foulcommit_away": match.get("fouls_away", 11),
                }
                matches_data.append(match_data)

            season_df = pd.DataFrame(matches_data)
            all_matches.append(season_df)
            print(f"{season}: {len(season_df)} matches\n")

            time.sleep(2)

        except Exception as e:
            print(f"Não enconctrada a temporada {season}: {e}\n")
            continue

    if all_matches:
        return pd.concat(all_matches, ignore_index=True)
    else:
        raise ValueError("Todas as fontes de dados falharam.")


def save_data_to_csv(df: pd.DataFrame, output_path: Path):
    """Salva o DataFrame em CSV."""
    # Verificar se o diretoria existe
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # limpar dados
    df = df.dropna()
    df = df.drop_duplicates()

    df.to_csv(output_path, index=False)

    print(f"\nData saved to: {output_path}")
    print(f"Final dataset: {len(df)} matches")
    print("\nDataset info:")
    print(df.info())
    print("\nSample statistics:")
    print(df.describe())


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("PREMIER LEAGUE DATA FETCHER")
    print("=" * 60 + "\n")

    output_path = Path("src/server/data/real_training_data.csv")

    try:
        # Try FBref first (most complete stats)
        df = fetch_latest_data(min_matches=500)

    except Exception as e:
        print(f"\n⚠ FBref failed: {e}")
        print("Trying alternative source...\n")

        try:
            # Fallback to WhoScored
            df = fallback_data(min_matches=500)
        except Exception as e2:
            print("\nAll sources failed!")
            print(f"FBref error: {e}")
            print(f"WhoScored error: {e2}")
            exit(1)

    save_data_to_csv(df, output_path)

    print("\n" + "=" * 60)
    print("DATA COLLECTION COMPLETE!")
    print("=" * 60 + "\n")
