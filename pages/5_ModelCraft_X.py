# modelcraft_router.py (or replace your existing router file)
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel
import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.metrics import get_scorer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.preprocessing import LabelEncoder

router = APIRouter(prefix="/modelcraft", tags=["ModelCraft-X"])

# Simple API key verification (change this to match your auth.py)
API_KEY_VALUE = "my-secret-key"


def verify_api_key(x_api_key: Optional[str] = Header(None)):
    if x_api_key != API_KEY_VALUE:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return True


class BenchmarkRequest(BaseModel):
    data: List[Dict[str, Any]]
    target: str


class BenchmarkResult(BaseModel):
    best_model: str
    metric: str
    final_score: float
    benchmark: List[Dict[str, Any]]


def prepare_data(df: pd.DataFrame, target: str):
    """Prepare X, y for ML with label encoding."""
    if target not in df.columns:
        raise ValueError(f"Target '{target}' not found in dataset")

    y = df[target]
    X = df.drop(columns=[target])

    # Encode categorical features
    for col in X.select_dtypes(include=['object']).columns:
        X[col] = LabelEncoder().fit_transform(X[col].astype(str))

    # Encode target if classification
    is_classification = y.dtype == 'object' or y.nunique() <= 20
    if is_classification:
        y = LabelEncoder().fit_transform(y.astype(str))

    return X, y, is_classification


@router.post("/benchmark", response_model=BenchmarkResult)
def benchmark(payload: BenchmarkRequest, dep=Depends(verify_api_key)):
    # Convert payload to DataFrame
    df = pd.DataFrame(payload.data)

    if df.empty:
        raise HTTPException(status_code=400, detail="Empty dataset")

    try:
        X, y, is_classification = prepare_data(df, payload.target)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Select models based on task type
    if is_classification:
        models = {
            "LogisticRegression": LogisticRegression(max_iter=1000),
            "RandomForestClassifier": RandomForestClassifier(n_estimators=50),
        }
        metric = "accuracy"
    else:
        models = {
            "LinearRegression": LinearRegression(),
            "RandomForestRegressor": RandomForestRegressor(n_estimators=50),
        }
        metric = "r2"

    results = []
    best_model_name = None
    best_score = -np.inf

    # Benchmark each model
    for name, model in models.items():
        try:
            scores = cross_val_score(model, X, y, cv=3, scoring=metric)
            mean_score = float(np.mean(scores))
        except Exception as e:
            mean_score = float("nan")

        results.append({
            "model": name,
            "score": mean_score,
            "type": "classification" if is_classification else "regression"
        })

        if not np.isnan(mean_score) and mean_score > best_score:
            best_score = mean_score
            best_model_name = name

    if best_model_name is None:
        best_model_name = "No valid model"
        best_score = 0.0

    return BenchmarkResult(
        best_model=best_model_name,
        metric=metric,
        final_score=round(best_score, 4),
        benchmark=results
    )
