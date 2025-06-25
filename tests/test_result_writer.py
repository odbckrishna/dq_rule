import os
import tempfile
import pandas as pd
from dq_rules.engine.result_writer import save_rule_results

def test_save_rule_results_creates_csv():
    results = [
        {'column': 'col1', 'rule': 'null_values', 'category': 'discovery', 'passed': True, 'observation': 'Null count: 0'},
        {'column': 'col2', 'rule': 'zscore', 'category': 'anomaly', 'passed': False, 'observation': 'Z-score outliers: 1'}
    ]
    with tempfile.TemporaryDirectory() as tmpdir:
        output_csv = os.path.join(tmpdir, 'results.csv')
        save_rule_results(results, output_csv)
        assert os.path.exists(output_csv)
        df = pd.read_csv(output_csv)
        assert 'column' in df.columns
        assert len(df) == 2
        assert df.loc[0, 'rule'] == 'null_values'
        assert df.loc[1, 'passed'] == False
