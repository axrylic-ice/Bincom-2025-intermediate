# pipeline.py
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

def build_pipeline(model):
    return Pipeline([
        ("preprocessing",StandardScaler()),
        ("model", model)
    ])
