# Anomaly category rules
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.svm import OneClassSVM
from sklearn.covariance import EllipticEnvelope
from scipy import stats

def zscore(series: pd.Series, threshold=3, hist_data_path=None, match_col='book_id', **kwargs):
    if hist_data_path is not None and match_col in kwargs:
        match_series = kwargs[match_col]
        hist_df = pd.read_csv(hist_data_path)
        merged = pd.DataFrame({'current': series, match_col: match_series}).dropna()
        # For each match_col, get the most recent historical value
        if 'business_date' in hist_df.columns:
            hist_latest = hist_df.sort_values('business_date').groupby(match_col)[series.name].last().reset_index()
        else:
            hist_latest = hist_df.groupby(match_col)[series.name].last().reset_index()
        merged = merged.merge(hist_latest, on=match_col, how='inner', suffixes=('', '_hist'))
        if merged.empty:
            return True, "No matching rows in history."
        diffs = merged['current'] - merged[series.name + '_hist']
        if diffs.std(ddof=0) == 0:
            return True, "No variation in differences, cannot compute z-score."
        z = np.abs((diffs - diffs.mean()) / diffs.std(ddof=0))
        outlier_idx = merged.index[z > threshold].tolist()
        if outlier_idx:
            example = merged.iloc[outlier_idx][[match_col, 'current', series.name + '_hist']].to_dict('records')
        else:
            example = []
    else:
        z = np.abs(stats.zscore(series.dropna()))
        outlier_idx = np.where(z > threshold)[0].tolist()
        example = series.dropna().iloc[outlier_idx].to_list() if outlier_idx else []
    outliers = len(outlier_idx)
    passed = outliers == 0
    obs = f"Z-score outliers: {outliers}"
    if example:
        obs += f"; Example: {example}"
    return passed, obs

def isolation_forest(series: pd.Series, contamination=0.05, hist_data_path=None, match_col='book_id', **kwargs):
    if hist_data_path is not None and match_col in kwargs:
        match_series = kwargs[match_col]
        hist_df = pd.read_csv(hist_data_path)
        merged = pd.DataFrame({'current': series, match_col: match_series}).dropna()
        merged = merged.merge(hist_df[[match_col, series.name]], on=match_col, how='inner', suffixes=('', '_hist'))
        if merged.empty:
            return True, "No matching rows in history."
        values = (merged['current'] - merged[series.name + '_hist']).values.reshape(-1, 1)
    else:
        values = series.dropna().values.reshape(-1, 1)
    model = IsolationForest(contamination=contamination, random_state=42)
    preds = model.fit_predict(values)
    outliers = (preds == -1).sum()
    passed = outliers == 0
    return passed, f"IsolationForest outliers: {outliers}"

def one_class_svm(series: pd.Series, **kwargs):
    model = OneClassSVM()
    preds = model.fit_predict(series.dropna().values.reshape(-1, 1))
    outliers = (preds == -1).sum()
    passed = outliers == 0
    return passed, f"OneClassSVM outliers: {outliers}"

def local_outlier_factor(series: pd.Series, **kwargs):
    model = LocalOutlierFactor()
    preds = model.fit_predict(series.dropna().values.reshape(-1, 1))
    outliers = (preds == -1).sum()
    passed = outliers == 0
    return passed, f"LOF outliers: {outliers}"

def elliptic_envelope(series: pd.Series, **kwargs):
    model = EllipticEnvelope()
    preds = model.fit_predict(series.dropna().values.reshape(-1, 1))
    outliers = (preds == -1).sum()
    passed = outliers == 0
    return passed, f"EllipticEnvelope outliers: {outliers}"
