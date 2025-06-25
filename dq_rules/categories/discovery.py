# Discovery category rules
import numpy as np
import pandas as pd

def null_values(series: pd.Series, **kwargs):
    null_count = series.isnull().sum()
    passed = null_count == 0
    return passed, f"Null count: {null_count}"

def duplicate_rows(series: pd.Series, **kwargs):
    dup_count = series.duplicated().sum()
    passed = dup_count == 0
    return passed, f"Duplicate count: {dup_count}"

def empty_strings(series: pd.Series, **kwargs):
    empty_count = (series == '').sum()
    passed = empty_count == 0
    return passed, f"Empty string count: {empty_count}"

def all_integers(series: pd.Series, **kwargs):
    is_int = pd.api.types.is_integer_dtype(series)
    passed = is_int
    return passed, f"Is integer dtype: {is_int}"

def all_strings(series: pd.Series, **kwargs):
    is_str = pd.api.types.is_string_dtype(series)
    passed = is_str
    return passed, f"Is string dtype: {is_str}"
