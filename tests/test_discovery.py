import pandas as pd
from dq_rules.categories.discovery import null_values, duplicate_rows, empty_strings, all_integers, all_strings
import numpy as np

def test_null_values():
    s = pd.Series([1, 2, None])
    passed, obs = null_values(s)
    assert not passed
    assert "Null count: 1" in obs

def test_duplicate_rows():
    s = pd.Series([1, 2, 2, 3])
    passed, obs = duplicate_rows(s)
    assert not passed
    assert "Duplicate count: 1" in obs

def test_empty_strings():
    s = pd.Series(["", "foo", "bar", ""])
    passed, obs = empty_strings(s)
    assert not passed
    assert "Empty string count: 2" in obs

def test_all_integers():
    s = pd.Series([1, 2, 3])
    passed, obs = all_integers(s)
    assert passed
    assert "Is integer dtype: True" in obs

def test_all_strings():
    s = pd.Series(["a", "b", "c"])
    passed, obs = all_strings(s)
    assert passed
    assert "Is string dtype: True" in obs
