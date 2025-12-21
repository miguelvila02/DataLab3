# 📊 Dashboard Usage Guide

Complete guide to using the Premier League Match Predictor Streamlit Dashboard.

## 🚀 Getting Started

### Launch the Dashboard

```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run dashboard
streamlit run dashboard.py
```

The dashboard will automatically open in your browser at `http://localhost:8501`

## 🎯 Dashboard Features

### Navigation

The dashboard has three main sections accessible from the sidebar:

1. **🎯 Make Prediction** - Enter team statistics and generate predictions
2. **📊 Analytics** - View model performance and metrics
3. **ℹ️ About** - Learn about the project

## 🏠 Make Prediction Tab

### Step 1: Enter Home Team Statistics

On the left side, you'll see **"Home Team - Last 5 Games"**:

1. **Expand each game** by clicking on "Game 1", "Game 2", etc.
2. **Enter statistics** for each of the last 5 games:
   - **Possession %**: Team's ball possession (0-100)
   - **Shots on Target**: Number of shots that were on target
   - **Corners**: Number of corner kicks
   - **Fouls**: Number of fouls committed

**Tips:**
- Start with the oldest game (Game 1) and work forward
- More recent games can be weighted more heavily in predictions
- All values must be non-negative numbers

### Step 2: Enter Away Team Statistics

On the right side, you'll see **"Away Team - Last 5 Games"**:

1. Follow the same process as for the home team
2. Enter statistics for each of the away team's last 5 games

**Example Values:**

**Home Team** (Strong team):
- Possession: 55-65%
- Shots on Target: 5-8
- Corners: 6-10
- Fouls: 8-12

**Away Team** (Weaker team):
- Possession: 35-45%
- Shots on Target: 2-4
- Corners: 3-5
- Fouls: 12-16

### Step 3: Generate Prediction

1. **Click** the green **"🔮 Generate Prediction"** button
2. **Wait** for the analysis (usually < 1 second)
3. **View** the results

### Understanding Results

#### Main Prediction

The prediction result shows:

- **Outcome**: Home Win, Draw, or Away Win
- **Confidence**: Percentage confidence in the prediction (0-100%)

**Confidence Levels:**
- **70-100%**: Very confident prediction
- **50-70%**: Moderate confidence
- **33-50%**: Low confidence (close match)

#### Probability Distribution Chart

A pie chart showing the probability of each outcome:

- **Green**: Home Win probability
- **Yellow**: Draw probability
- **Red**: Away Win probability

**How to interpret:**
- Larger slice = More likely outcome
- Similar sized slices = Uncertain match
- Dominant slice (>60%) = Clear favorite

#### Team Statistics Comparison Chart

A bar chart comparing average statistics:

- **Green bars**: Home team
- **Red bars**: Away team

**What to look for:**
- **Possession**: Higher = more control of the game
- **Shots**: More shots on target = more attacking threat
- **Corners**: Indicates attacking pressure
- **Fouls**: Higher fouls may indicate defensive play

#### Detailed Statistics Tables

Two tables showing averaged statistics for each team:

- **Home Team Averages**: Mean values across their 5 games
- **Away Team Averages**: Mean values across their 5 games

## 📊 Analytics Tab

### Model Performance Metrics

Three key metrics displayed prominently:

1. **Model Accuracy**: Overall prediction accuracy (70%+)
2. **Training Matches**: Number of matches used for training (500+)
3. **Key Features**: Number of statistical features used (8)

### Features Used

List of the 8 features the model considers:

- Possession %
- Shots on Target  
- Corners
- Fouls

(Each stat is compared between home and away teams)

### Model Details

Technical information about the model:

- **Algorithm**: Random Forest Classifier
- **Number of Trees**: 150 decision trees
- **Max Depth**: 12 levels deep
- **Training Period**: 2021-2024 seasons
- **Update Frequency**: Weekly updates with new data

### Historical Accuracy Chart

Line graph showing model accuracy improvement over time:

- **X-axis**: Season (2021-2022, 2022-2023, 2023-2024)
- **Y-axis**: Accuracy percentage
- **Trend**: Shows model is improving with more data

## ℹ️ About Tab

### Overview

High-level explanation of what the project does and how it works.

### How It Works

Step-by-step breakdown:

1. **Data Collection**: You input team statistics
2. **Feature Engineering**: System calculates averages
3. **Model Analysis**: Random Forest processes the data
4. **Prediction**: System generates outcome with confidence

### Technology Stack

Lists all technologies used:

- **Backend**: Python, scikit-learn, FastAPI
- **Frontend**: Streamlit, Plotly
- **Data**: soccerdata, pandas, numpy
- **Deployment**: Docker, uvicorn

### Project Structure

Shows the directory layout of the project.

### Authors & Contact

Information about the creators and how to get in touch.

## 💡 Pro Tips

### Getting Better Predictions

1. **Use Recent Data**: More recent games are generally more indicative
2. **Consider Context**: Cup games vs league games may have different patterns
3. **Home Advantage**: Home teams typically have 5-10% more possession
4. **Check All Stats**: Don't rely on just one statistic

### Example Scenarios

#### Scenario 1: Clear Home Win

**Home Team**:
- Possession: 60%+ consistently
- Shots: 7+ per game
- Few fouls (8-10)

**Away Team**:
- Possession: 40%- consistently
- Shots: 2-3 per game
- Many fouls (14-16)

**Expected**: Home Win with 60-70% confidence

#### Scenario 2: Even Match (Likely Draw)

**Both Teams**:
- Possession: Around 50%
- Similar shots on target
- Similar corners and fouls

**Expected**: Any outcome with 35-45% confidence

#### Scenario 3: Upset Potential

**Home Team**:
- Possession: 45-50%
- Shots: 3-4 per game
- High fouls (13-15)

**Away Team**:
- Possession: 50-55%
- Shots: 6-7 per game
- Low fouls (9-11)

**Expected**: Away Win or Draw with moderate confidence

### Common Patterns

**Dominant Home Team:**
- Possession: 58-65%
- Shots on Target: 6-9
- Corners: 7-10
- Fouls: 8-11

**Struggling Away Team:**
- Possession: 35-42%
- Shots on Target: 2-3
- Corners: 3-5
- Fouls: 13-17

**Defensive Team:**
- Low possession (40-45%)
- Few shots (2-4)
- Few corners (3-5)
- Many fouls (14-18)

**Attacking Team:**
- High possession (55-62%)
- Many shots (7-10)
- Many corners (8-12)
- Moderate fouls (9-12)

## 🔧 Troubleshooting

### Dashboard Won't Load

**Solution:**
```bash
# Check if Streamlit is installed
pip list | grep streamlit

# Reinstall if needed
pip install streamlit

# Check port availability
streamlit run dashboard.py --server.port 8502
```

### Prediction Button Not Working

**Possible causes:**
1. Missing model file
2. Invalid input values
3. All values are zero

**Solutions:**
- Ensure model is trained: `python model_trainer.py`
- Check that all inputs are valid numbers
- Enter realistic values (possession > 0, etc.)

### Chart Not Displaying

**Solution:**
- Refresh the page (F5)
- Clear Streamlit cache: Click ☰ → Clear cache
- Update Plotly: `pip install --upgrade plotly`

### Slow Performance

**Solutions:**
- Close other browser tabs
- Reduce number of games (use 3-4 instead of 5)
- Check system resources
- Restart the dashboard

## 🎨 Customization

### Change Theme

Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#10b981"  # Green
backgroundColor = "#1e293b"  # Dark blue
secondaryBackgroundColor = "#334155"  # Medium blue
textColor = "#ffffff"  # White
font = "sans serif"
```

### Modify Default Values

Edit `dashboard.py`:

```python
# Find create_game_inputs function
possession = st.number_input(
    "Possession %",
    value=YOUR_DEFAULT_VALUE,  # Change this
    step=0.1
)
```

## 📱 Mobile Usage

The dashboard is responsive and works on mobile devices:

1. **Access** via mobile browser at `http://YOUR_IP:8501`
2. **Sidebar** can be collapsed for more space
3. **Charts** are touch-interactive
4. **Inputs** use mobile-optimized number pads

## 🔗 Integration with API

The dashboard can be used alongside the REST API:

```bash
# Terminal 1: Run API
uvicorn main:app --reload

# Terminal 2: Run Dashboard
streamlit run dashboard.py
```

Access both:
- Dashboard: http://localhost:8501
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📈 Best Practices

1. **Regular Updates**: Keep statistics up-to-date
2. **Compare Predictions**: Use both dashboard and API
3. **Track Accuracy**: Note predictions and compare with actual results
4. **Understand Limitations**: Model is ~70% accurate, not perfect
5. **Consider Context**: Injuries, weather, and motivation affect outcomes

## 🆘 Getting Help

If you encounter issues:

1. **Check this guide** for common solutions
2. **Read the logs** in the terminal running the dashboard
3. **Restart the dashboard**: `Ctrl+C` then run again
4. **GitHub Issues**: Report bugs or ask questions
5. **Email**: luismiguelvila@gmail.com

## 📚 Additional Resources

- **README.md**: Project overview
- **QUICKSTART.md**: Fast setup guide
- **CONFIGURATION.md**: Advanced configuration
- **API Docs**: http://localhost:8000/docs

---

**Happy Predicting! ⚽📊**

*Last updated: December 2024*