"""Offline 5-fold CV of the supervised baselines on the collected flow features (result.csv)."""
import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

# columns: sfe, ssip, rfip, label (0 normal, 1 attack)
data = np.loadtxt("result.csv", delimiter=",")
X, y = data[:, :3], data[:, 3]

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
models = {
    "DecisionTree": DecisionTreeClassifier(random_state=0),
    "SVC (RBF)": SVC(),
}

print(f"{len(y)} samples ({int(y.sum())} attack / {int((y == 0).sum())} normal)")
for name, model in models.items():
    scores = cross_validate(model, X, y, cv=cv, scoring=["accuracy", "precision", "recall", "f1"])
    summary = ", ".join(f"{m}={scores['test_' + m].mean():.3f}" for m in ["accuracy", "precision", "recall", "f1"])
    print(f"{name:14s} {summary}")
