import pandas as pd
import numpy as np
from dq_rules.categories.anomaly import zscore, isolation_forest, one_class_svm, local_outlier_factor, elliptic_envelope

def test_zscore():
    s = pd.Series([1, 2, 3, 100])
    passed, obs = zscore(s, threshold=2)
    assert passed is True or passed is np.bool_(True) or passed == True
    assert "outliers" in obs

def test_isolation_forest():
    s = pd.Series([1, 2, 3, 100])
    passed, obs = isolation_forest(s, contamination=0.25)
    assert not passed
    assert "outliers" in obs

def test_one_class_svm():
    s = pd.Series([1, 2, 3, 100])
    passed, obs = one_class_svm(s)
    assert not passed
    assert "outliers" in obs

def test_local_outlier_factor():
    s = pd.Series([1, 2, 3, 100])
    passed, obs = local_outlier_factor(s)
    assert passed is True or passed is np.bool_(True) or passed == True
    assert "outliers" in obs

def test_elliptic_envelope():
    s = pd.Series([1, 2, 3, 100])
    passed, obs = elliptic_envelope(s)
    assert not passed
    assert "outliers" in obs
