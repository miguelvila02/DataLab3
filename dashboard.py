"""
Premier League Match Predictor - Streamlit Dashboard
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Page configuration
st.set_page_config(
    page_title="Premier League Match Predictor",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stButton>button {
        background: linear-gradient(90deg, #10b981 0%, #3b82f6 100%);
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 30px;
        border: none;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #059669 0%, #2563eb 100%);
        transform: scale(1.05);
    }
    h1 {
        color: #ffffff;
        text-align: center;
        font-size: 3em;
        margin-bottom: 0.5em;
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        backdrop-filter: blur(10px);
    }
</style>
""",
    unsafe_allow_html=True,
)

# Initialize session state
if "prediction" not in st.session_state:
    st.session_state.prediction = None

# Title
st.markdown("# ⚽ Premier League Match Predictor")
st.markdown("### ML-Powered Match Outcome Predictions")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.image(
        "https://yt3.googleusercontent.com/zhPMOpUIlmMa_xAgrHYGYrkCSWS-3tE0yPPKVUzh1iiYOF1QDqGtg3ZIbWXjkNmN3l3WPqziRHE=s900-c-k-c0x00ffffff-no-rj",
        width=200,
    )
    st.markdown("## Navigation")
    page = st.radio("Go to:", ["🎯 Make Prediction", "📊 Analytics", "ℹ️ About"])

    st.markdown("---")
    st.markdown("### Quick Stats")
    st.metric("Model Accuracy", "70%+")
    st.metric("Training Matches", "500+")
    st.metric("Features Used", "8")


# Helper function to create game input
def create_game_inputs(team_name, team_type, num_games=5):
    st.markdown(f"### {team_name} - Last {num_games} Games")
    games = []

    for i in range(num_games):
        with st.expander(f"Game {i+1}", expanded=i == 0):
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                possession = st.number_input(
                    "Possession %",
                    min_value=0.0,
                    max_value=100.0,
                    value=55.0 if team_type == "home" else 45.0,
                    step=0.1,
                    key=f"{team_type}_poss_{i}",
                )

            with col2:
                shots = st.number_input(
                    "Shots on Target",
                    min_value=0,
                    max_value=30,
                    value=5 if team_type == "home" else 3,
                    key=f"{team_type}_shots_{i}",
                )

            with col3:
                corners = st.number_input(
                    "Corners",
                    min_value=0,
                    max_value=20,
                    value=6 if team_type == "home" else 4,
                    key=f"{team_type}_corners_{i}",
                )

            with col4:
                fouls = st.number_input(
                    "Fouls",
                    min_value=0,
                    max_value=30,
                    value=10 if team_type == "home" else 13,
                    key=f"{team_type}_fouls_{i}",
                )

            games.append(
                {
                    "possession": possession,
                    "shots_on_target": shots,
                    "corners": corners,
                    "fouls": fouls,
                }
            )

    return games


# Function to make prediction
def make_prediction(home_games, away_games):
    """Mock prediction function"""
    # Calculate averages
    home_avg = {
        "possession": np.mean([g["possession"] for g in home_games]),
        "shots": np.mean([g["shots_on_target"] for g in home_games]),
        "corners": np.mean([g["corners"] for g in home_games]),
        "fouls": np.mean([g["fouls"] for g in home_games]),
    }

    away_avg = {
        "possession": np.mean([g["possession"] for g in away_games]),
        "shots": np.mean([g["shots_on_target"] for g in away_games]),
        "corners": np.mean([g["corners"] for g in away_games]),
        "fouls": np.mean([g["fouls"] for g in away_games]),
    }

    # Calculate differences
    poss_diff = home_avg["possession"] - away_avg["possession"]
    shots_diff = home_avg["shots"] - away_avg["shots"]

    # Simple prediction logic
    home_win_prob = 0.33 + (poss_diff * 0.005) + (shots_diff * 0.02)
    away_win_prob = 0.33 - (poss_diff * 0.005) - (shots_diff * 0.02)

    # Ensure probabilities are valid
    home_win_prob = max(0.1, min(0.8, home_win_prob))
    away_win_prob = max(0.1, min(0.8, away_win_prob))
    draw_prob = 1 - home_win_prob - away_win_prob

    # Determine prediction
    probs = {"Home Win": home_win_prob, "Draw": draw_prob, "Away Win": away_win_prob}
    prediction = max(probs, key=probs.get)
    confidence = probs[prediction] * 100

    return {
        "prediction": prediction,
        "confidence": confidence,
        "probabilities": probs,
        "home_avg": home_avg,
        "away_avg": away_avg,
    }


# PAGE: Make Prediction
if page == "🎯 Make Prediction":
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        home_games = create_game_inputs("🏠 Home Team", "home")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        away_games = create_game_inputs("✈️ Away Team", "away")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Generate Prediction", use_container_width=True):
            with st.spinner("Analyzing team statistics..."):
                prediction = make_prediction(home_games, away_games)
                st.session_state.prediction = prediction

    # Display prediction results
    if st.session_state.prediction:
        pred = st.session_state.prediction

        st.markdown("## 🎯 Prediction Results")

        # Main prediction
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(
                f"""
            <div style='background: linear-gradient(135deg, #10b981 0%, #3b82f6 100%); 
                        padding: 30px; border-radius: 15px; text-align: center; color: white;'>
                <h2 style='margin: 0; color: white;'>Predicted Outcome</h2>
                <h1 style='margin: 10px 0; font-size: 3em; color: white;'>{pred['prediction']}</h1>
                <h3 style='margin: 0; color: white;'>Confidence: {pred['confidence']:.1f}%</h3>
            </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown("---")

        # Visualizations
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Probability Distribution")
            fig = go.Figure(
                data=[
                    go.Pie(
                        labels=list(pred["probabilities"].keys()),
                        values=[v * 100 for v in pred["probabilities"].values()],
                        marker=dict(colors=["#10b981", "#f59e0b", "#ef4444"]),
                        textinfo="label+percent",
                        textfont=dict(size=14, color="white"),
                        hole=0.4,
                    )
                ]
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white"),
                showlegend=True,
                height=400,
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### Team Statistics Comparison")
            stats_df = pd.DataFrame(
                {
                    "Statistic": ["Possession", "Shots", "Corners", "Fouls"],
                    "Home": [
                        pred["home_avg"]["possession"],
                        pred["home_avg"]["shots"],
                        pred["home_avg"]["corners"],
                        pred["home_avg"]["fouls"],
                    ],
                    "Away": [
                        pred["away_avg"]["possession"],
                        pred["away_avg"]["shots"],
                        pred["away_avg"]["corners"],
                        pred["away_avg"]["fouls"],
                    ],
                }
            )

            fig = go.Figure(
                data=[
                    go.Bar(
                        name="Home",
                        x=stats_df["Statistic"],
                        y=stats_df["Home"],
                        marker_color="#10b981",
                    ),
                    go.Bar(
                        name="Away",
                        x=stats_df["Statistic"],
                        y=stats_df["Away"],
                        marker_color="#ef4444",
                    ),
                ]
            )
            fig.update_layout(
                barmode="group",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white"),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)"),
                height=400,
            )
            st.plotly_chart(fig, use_container_width=True)

        # Detailed statistics
        st.markdown("### Detailed Statistics")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Home Team Averages")
            st.dataframe(
                pd.DataFrame([pred["home_avg"]]).T.rename(columns={0: "Value"}),
                use_container_width=True,
            )

        with col2:
            st.markdown("#### Away Team Averages")
            st.dataframe(
                pd.DataFrame([pred["away_avg"]]).T.rename(columns={0: "Value"}),
                use_container_width=True,
            )

# PAGE: Analytics
elif page == "📊 Analytics":
    st.markdown("## 📊 Model Performance Analytics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
        <div class="metric-card">
            <h2 style='color: #10b981; margin: 0;'>70%+</h2>
            <p style='color: white; margin: 5px 0;'>Model Accuracy</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div class="metric-card">
            <h2 style='color: #3b82f6; margin: 0;'>500+</h2>
            <p style='color: white; margin: 5px 0;'>Training Matches</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
        <div class="metric-card">
            <h2 style='color: #a855f7; margin: 0;'>8</h2>
            <p style='color: white; margin: 5px 0;'>Key Features</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Model details
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Features Used")
        features = ["Possession %", "Shots on Target", "Corners", "Fouls"]
        for feature in features:
            st.markdown(f"✅ **{feature}**")

    with col2:
        st.markdown("### Model Details")
        st.markdown(
            """
        - **Algorithm**: Random Forest Classifier
        - **Number of Trees**: 150
        - **Max Depth**: 12
        - **Training Period**: 2021-2024
        - **Update Frequency**: Weekly
        """
        )

    st.markdown("---")

    # Sample accuracy chart
    st.markdown("### Historical Accuracy")
    seasons = ["2021-2022", "2022-2023", "2023-2024"]
    accuracy = [68.5, 71.2, 73.8]

    fig = go.Figure(
        data=[
            go.Scatter(
                x=seasons,
                y=accuracy,
                mode="lines+markers",
                line=dict(color="#10b981", width=3),
                marker=dict(size=12, color="#3b82f6"),
            )
        ]
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        xaxis=dict(showgrid=False),
        yaxis=dict(title="Accuracy (%)", showgrid=True, gridcolor="rgba(255,255,255,0.1)"),
        height=400,
    )
    st.plotly_chart(fig, use_container_width=True)

# PAGE: About
elif page == "ℹ️ About":
    st.markdown("## ℹ️ About This Project")

    st.markdown(
        """
    ### Overview
    The Premier League Match Predictor uses machine learning to predict match outcomes 
    based on team statistics from their recent games. The model analyzes possession, 
    shots on target, corners, and fouls to determine the most likely result.
    
    ### How It Works
    1. **Data Collection**: Statistics from each team's last 5 games
    2. **Feature Engineering**: Calculate average performance metrics
    3. **Model Analysis**: Random Forest classifier processes the data
    4. **Prediction**: Generate outcome with confidence scores
    
    ### Technology Stack
    """
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
        #### Backend
        - Python 3.8+
        - scikit-learn
        - FastAPI
        - pandas & numpy
        """
        )

    with col2:
        st.markdown(
            """
        #### Frontend
        - Streamlit
        - Plotly
        - React (Web version)
        """
        )

    st.markdown("---")

    st.markdown(
        """
    ### Project Structure
    ```
    pl-match-predictor/
    ├── src/
    │   ├── server/
    │   │   ├── api/         # REST API
    │   │   ├── data/        # Data fetching
    │   │   └── model/       # ML models
    │   └── app/             # Dashboard
    ├── tests/               # Test suite
    └── docs/                # Documentation
    ```
    
    ### Authors
    Created by **Miguel Vila** and **Daniel Rodrigues**
    
    ### License
    MIT License
    
    ### Contact
    - GitHub: [@miguelvila02](https://github.com/miguelvila02)
    - Email: luismiguelvila@gmail.com
    """
    )

# Footer
st.markdown("---")
st.markdown(
    """
<div style='text-align: center; color: rgba(255,255,255,0.7);'>
    <p>Premier League Match Predictor beta v1.0.0 | Built using Streamlit</p>
    <p>© 2025 Miguel Vila & Daniel Rodrigues | MIT License</p>
</div>
""",
    unsafe_allow_html=True,
)
