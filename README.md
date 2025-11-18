# DataLab3

Why use RandomForest and not Logistic Regression?
Logistic Regression assumes a linear relationship between the features and the log-odds
of the outcome.Footbll is more complex than that, so it is outperformed by a tree based model.

Why are you dropping these columns? The target variable is the outcome of the match.
We need to create a target variable based on the goals scored.
For simplicity, let's define the target as 1 if home team wins, 0 for draw, and -1 for away team wins.

