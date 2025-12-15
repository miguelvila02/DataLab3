import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Dict


def load_model(model_path: str = 'model/match_predictor.joblib'):
    """Load the trained model from joblib file"""
    return joblib.load(model_path)


def calculate_avg_stats(last_5_games: List[Dict]) -> Dict[str, float]:
    """
    Calculate average statistics from the last 5 games.
    
    Args:
        last_5_games: List of dictionaries containing game statistics
                     Each dict should have: possession, shots_on_target, corners, fouls
    
    Returns:
        Dictionary with averaged statistics
    """
    if not last_5_games:
        raise ValueError("Need at least 1 game in history")
    
    df = pd.DataFrame(last_5_games)
    
    return {
        'avg_possession': df['possession'].mean(),
        'avg_shots_on_target': df['shots_on_target'].mean(),
        'avg_corners': df['corners'].mean(),
        'avg_fouls': df['fouls'].mean()
    }


def predict_from_recent_form(
    home_team_last_5: List[Dict],
    away_team_last_5: List[Dict],
    model_path: str = 'server/src/model/match_predictor.joblib'
) -> dict:
    """
    Predict match outcome based on teams' last 5 games statistics.
    
    Args:
        home_team_last_5: List of dicts with stats from home team's last 5 games
                         Each dict: {'possession': float, 'shots_on_target': int, 
                                    'corners': int, 'fouls': int}
        away_team_last_5: List of dicts with stats from away team's last 5 games
        model_path: Path to the saved model file
    
    Returns:
        Dictionary with prediction, probabilities, and team averages
    """
    # Calculate average statistics
    home_avg = calculate_avg_stats(home_team_last_5)
    away_avg = calculate_avg_stats(away_team_last_5)
    
    # Load model
    model = load_model(model_path)
    
    # Create feature DataFrame with correct column names
    features = pd.DataFrame({
        'possession_home': [home_avg['avg_possession']],
        'possession_away': [away_avg['avg_possession']],
        'shoton_home': [home_avg['avg_shots_on_target']],
        'shoton_away': [away_avg['avg_shots_on_target']],
        'corner_home': [home_avg['avg_corners']],
        'corner_away': [away_avg['avg_corners']],
        'foulcommit_home': [home_avg['avg_fouls']],
        'foulcommit_away': [away_avg['avg_fouls']]
    })
    
    # Make prediction
    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]
    
    # Map prediction to outcome
    outcome_map = {1: 'Home Win', 0: 'Draw', -1: 'Away Win'}
    classes = model.classes_
    prob_dict = {outcome_map[cls]: prob for cls, prob in zip(classes, probabilities)}
    
    return {
        'prediction': outcome_map[prediction],
        'prediction_code': prediction,
        'probabilities': prob_dict,
        'confidence': max(probabilities) * 100,
        'home_team_averages': home_avg,
        'away_team_averages': away_avg
    }


def predict_with_custom_weights(
    home_team_last_5: List[Dict],
    away_team_last_5: List[Dict],
    weights: List[float] = None,
    model_path: str = 'model/match_predictor.joblib'
) -> dict:

    if weights is None:
        # Default: more weight to recent games
        weights = [0.1, 0.15, 0.2, 0.25, 0.3]
    
    if len(weights) != len(home_team_last_5):
        raise ValueError("Weights length must match number of games")
    
    weights = np.array(weights)
    weights = weights / weights.sum()  # Normalize
    
    def weighted_avg(games_list: List[Dict]) -> Dict[str, float]:
        df = pd.DataFrame(games_list)
        return {
            'avg_possession': (df['possession'] * weights).sum(),
            'avg_shots_on_target': (df['shots_on_target'] * weights).sum(),
            'avg_corners': (df['corners'] * weights).sum(),
            'avg_fouls': (df['fouls'] * weights).sum()
        }
    
    home_avg = weighted_avg(home_team_last_5)
    away_avg = weighted_avg(away_team_last_5)
    
    # Load model and predict
    model = load_model(model_path)
    
    features = pd.DataFrame({
        'possession_home': [home_avg['avg_possession']],
        'possession_away': [away_avg['avg_possession']],
        'shoton_home': [home_avg['avg_shots_on_target']],
        'shoton_away': [away_avg['avg_shots_on_target']],
        'corner_home': [home_avg['avg_corners']],
        'corner_away': [away_avg['avg_corners']],
        'foulcommit_home': [home_avg['avg_fouls']],
        'foulcommit_away': [away_avg['avg_fouls']]
    })
    
    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]
    
    outcome_map = {1: 'Home Win', 0: 'Draw', -1: 'Away Win'}
    classes = model.classes_
    prob_dict = {outcome_map[cls]: prob for cls, prob in zip(classes, probabilities)}
    
    return {
        'prediction': outcome_map[prediction],
        'prediction_code': prediction,
        'probabilities': prob_dict,
        'confidence': max(probabilities) * 100,
        'home_team_weighted_avg': home_avg,
        'away_team_weighted_avg': away_avg,
        'weights_used': weights.tolist()
    }


# Example usage
if __name__ == "__main__":
    # Example: Last 5 games for home team (oldest to newest)
    home_team_games = [
        {'possession': 52, 'shots_on_target': 4, 'corners': 5, 'fouls': 11},
        {'possession': 48, 'shots_on_target': 3, 'corners': 4, 'fouls': 13},
        {'possession': 55, 'shots_on_target': 1, 'corners': 8, 'fouls': 9},
        {'possession': 60, 'shots_on_target': 2, 'corners': 7, 'fouls': 10},
        {'possession': 58, 'shots_on_target': 3, 'corners': 9, 'fouls': 8}
    ]
    
    # Example: Last 5 games for away team (oldest to newest)
    away_team_games = [
        {'possession': 45, 'shots_on_target': 2, 'corners': 3, 'fouls': 15},
        {'possession': 50, 'shots_on_target': 5, 'corners': 6, 'fouls': 12},
        {'possession': 47, 'shots_on_target': 3, 'corners': 4, 'fouls': 14},
        {'possession': 43, 'shots_on_target': 5, 'corners': 3, 'fouls': 16},
        {'possession': 46, 'shots_on_target': 4, 'corners': 5, 'fouls': 13}
    ]
    
    print("="*60)
    print("SIMPLE AVERAGE PREDICTION (Equal weight for all 5 games)")
    print("="*60)
    result = predict_from_recent_form(home_team_games, away_team_games)
    
    print(f"\n🏠 Home Team Averages (Last 5 games):")
    for stat, value in result['home_team_averages'].items():
        print(f"   {stat}: {value:.2f}")
    
    print(f"\n✈️  Away Team Averages (Last 5 games):")
    for stat, value in result['away_team_averages'].items():
        print(f"   {stat}: {value:.2f}")
    
    print(f"\n🎯 PREDICTION: {result['prediction']}")
    print(f"📊 Confidence: {result['confidence']:.2f}%")
    print(f"\n📈 Win Probabilities:")
    for outcome, prob in result['probabilities'].items():
        print(f"   {outcome}: {prob*100:.2f}%")
    
    print("\n" + "="*60)
    print("WEIGHTED PREDICTION (Recent games weighted higher)")
    print("="*60)
    weighted_result = predict_with_custom_weights(home_team_games, away_team_games)
    
    print(f"\n⚖️  Weights used: {weighted_result['weights_used']}")
    print(f"   (Oldest game → Newest game)")
    
    print(f"\n🏠 Home Team Weighted Averages:")
    for stat, value in weighted_result['home_team_weighted_avg'].items():
        print(f"   {stat}: {value:.2f}")
    
    print(f"\n✈️  Away Team Weighted Averages:")
    for stat, value in weighted_result['away_team_weighted_avg'].items():
        print(f"   {stat}: {value:.2f}")
    
    print(f"\n🎯 PREDICTION: {weighted_result['prediction']}")
    print(f"📊 Confidence: {weighted_result['confidence']:.2f}%")
    print(f"\n📈 Win Probabilities:")
    for outcome, prob in weighted_result['probabilities'].items():
        print(f"   {outcome}: {prob*100:.2f}%")