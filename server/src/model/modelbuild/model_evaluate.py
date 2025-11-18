import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import confusion_matrix
import numpy as np

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
model = RandomForestClassifier(n_estimators=150, random_state=42)

model.fit(X_train, Y_train)

Y_pred = model.predict(X_test)


def evaluate_model(y_true, y_pred):
    accuracy = accuracy_score(y_true, y_pred)
    report = classification_report(y_true, y_pred)
    cm = confusion_matrix(y_true, y_pred)

    print(f"Accuracy: {accuracy:.2f}")
    print("Classification Report:")
    print(report)

    plt.figure(figsize=(8, 6))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Confusion Matrix')
    plt.colorbar()
    tick_marks = np.arange(len(set(y_true)))
    plt.xticks(tick_marks, set(y_true))
    plt.yticks(tick_marks, set(y_true))

    thresh = cm.max() / 2.
    for i, j in np.ndindex(cm.shape):
        plt.text(j, i, format(cm[i, j], 'd'),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()
    plt.show()


evaluate_model(Y_test, Y_pred)

