# ⚽ premier league match predictor

predict match results using machine learning. random forest classifier trained on match data.

## what it does

predicts home win / draw / away win based on:
- possession %
- shots on target
- corners
- fouls

accuracy around 70% on test data.

## setup

```bash
git clone https://github.com/miguelvila02/pl-match-predictor.git
cd pl-match-predictor

python -m venv venv
source venv/bin/activate  # windows: venv\Scripts\activate

pip install -r requirements.txt
```

## usage

### 1. get data

```bash
python get_data.py
```

generates sample data or fetches real matches if soccerdata library available.

### 2. train model

```bash
python model_trainer.py
```

trains random forest, saves to `models/random_forest_model.pkl`

### 3. run dashboard

```bash
streamlit run dashboard.py
```

opens at http://localhost:8501

### or run api

```bash
uvicorn main:app --reload
```

docs at http://localhost:8000/docs

## using the dashboard

1. enter stats for last 5 games (both teams)
2. click predict
3. see result + confidence + charts

typical values:
- possession: 30-70%
- shots on target: 1-10
- corners: 2-12
- fouls: 5-20

## project structure

```
├── get_data.py          # data generation
├── model_trainer.py     # model training
├── dashboard.py         # streamlit ui
├── main.py             # fastapi
├── data/               # training data
├── models/             # saved models
└── tests/              # tests
```

## model details

- algorithm: random forest
- trees: 150
- max depth: 12
- features: 6 (possession diff, shots diff, etc)
- training: 2021-2024 seasons

## making predictions

dashboard is easiest. enter game stats, get instant result.

api example:
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "home_team_last_5": [
      {"possession": 55, "shots_on_target": 5, "corners": 6, "fouls": 10}
    ],
    "away_team_last_5": [
      {"possession": 45, "shots_on_target": 3, "corners": 4, "fouls": 13}
    ]
  }'
```

## testing

```bash
pytest tests/ -v
```

## docker

```bash
docker build -t pl-predictor .
docker run -p 8000:8000 pl-predictor
```

or

```bash
docker-compose up
```

## makefile commands

```bash
make install        # install deps
make fetch-data     # get data
make train-model    # train
make run-dashboard  # start streamlit
make run-api        # start fastapi
make test          # run tests
make clean         # cleanup
```

## data sources

- sample data: generated based on pl averages
- real data: fbref via soccerdata library (optional)

## known issues

- need model file before using dashboard (run model_trainer.py first)
- port 8501 might be in use, change with `--server.port 8502`
- requires training data (run get_data.py first)

## todo

- [ ] more features (xG, head-to-head)
- [ ] better model (neural net maybe)
- [ ] live data integration
- [ ] mobile app
- [ ] other leagues

## tech stack

python, scikit-learn, pandas, numpy, streamlit, fastapi, plotly, docker

## contributing

fork, make changes, open PR. run tests first.

## license

mit

## authors

miguel vila & daniel rodrigues

contact: luismiguelvila@gmail.com

---

built for a uni project. works pretty well but not perfect. ~70% accuracy seems ok for football predictions.