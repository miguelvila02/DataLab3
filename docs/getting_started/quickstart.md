# quick setup

get this running in 5 minutes.

## what you need

- python 3.8+
- pip
- git

## steps

### 1. clone it

```bash
git clone https://github.com/miguelvila02/pl-match-predictor.git
cd pl-match-predictor
```

### 2. virtual env

**windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**mac/linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. install stuff

```bash
pip install -r requirements.txt
```

takes a minute or two.

### 4. get data

```bash
python get_data.py
```

creates sample data in `data/premier_league_matches.csv`

want real data? it'll try to fetch from fbref automatically. takes longer (5-10 min).

### 5. train model

```bash
python model_trainer.py
```

trains the random forest. saves to `models/random_forest_model.pkl`

### 6. run it

#### dashboard (recommended)

```bash
streamlit run dashboard.py
```

browser opens at http://localhost:8501

#### or api

```bash
uvicorn main:app --reload
```

check http://localhost:8000/docs

## using the dashboard

super simple:

1. open http://localhost:8501
2. enter stats for each team (last 5 games)
3. click predict
4. done

stats to enter:
- possession (0-100)
- shots on target (usually 0-10)
- corners (usually 2-12)
- fouls (usually 5-20)

## problems?

### "module not found"

forgot to activate venv? or install requirements?

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "port already in use"

try different port:

```bash
streamlit run dashboard.py --server.port 8502
```

### "model file not found"

train it first:

```bash
python model_trainer.py
```

### "data file not found"

generate it:

```bash
python get_data.py
```

## what's where

```
pl-match-predictor/
├── data/
│   └── premier_league_matches.csv    # training data
├── models/
│   └── random_forest_model.pkl       # trained model
├── get_data.py                       # data script
├── model_trainer.py                  # training script
├── dashboard.py                      # streamlit app
└── main.py                          # fastapi
```

## tips

- sample data works fine for testing
- dashboard is easier than api for one-off predictions
- model takes ~30 seconds to train
- default stats in forms are reasonable

## next

play with it. try different stats. see what happens.

the model isn't perfect (70% accuracy) but that's decent for football.

---

questions? check README.md or email luismiguelvila@gmail.com