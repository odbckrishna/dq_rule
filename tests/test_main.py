import os
import tempfile
import yaml
import pandas as pd
import pytest
from dq_rules.main import main
from dq_rules.engine.rule_engine import RuleEngine

def create_sample_yaml(yaml_path, csv_path):
    config = {
        'dataset_name': 'test_dataset',
        'data_path': csv_path,
        'rules': {
            'col1': [
                {'category': 'discovery', 'name': 'null_values', 'params': {}}
            ]
        }
    }
    with open(yaml_path, 'w') as f:
        yaml.dump(config, f)

def create_sample_csv(csv_path):
    df = pd.DataFrame({'col1': [1, 2, None]})
    df.to_csv(csv_path, index=False)

def test_main_runs_and_outputs_csv():
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_path = os.path.join(tmpdir, 'data.csv')
        yaml_path = os.path.join(tmpdir, 'test_dataset.yml')
        output_csv = os.path.join(tmpdir, 'result.csv')
        create_sample_csv(csv_path)
        create_sample_yaml(yaml_path, csv_path)
        # Copy the discovery.py module to the temp dir structure for import
        import shutil
        import sys
        dq_rules_dir = os.path.join(tmpdir, 'dq_rules')
        categories_dir = os.path.join(dq_rules_dir, 'categories')
        engine_dir = os.path.join(dq_rules_dir, 'engine')
        os.makedirs(categories_dir)
        os.makedirs(engine_dir)
        # Copy required modules
        from pathlib import Path
        orig_discovery = Path(__file__).parent.parent / 'dq_rules' / 'categories' / 'discovery.py'
        orig_engine = Path(__file__).parent.parent / 'dq_rules' / 'engine' / 'rule_engine.py'
        shutil.copy(orig_discovery, categories_dir)
        shutil.copy(orig_engine, engine_dir)
        # Patch sys.path for import
        sys.path.insert(0, tmpdir)
        # Patch onboarding path
        orig_dir = os.getcwd()
        os.chdir(tmpdir)
        try:
            main('test_dataset', output_csv)
            assert os.path.exists(output_csv)
            df = pd.read_csv(output_csv)
            assert 'passed' in df.columns
        finally:
            os.chdir(orig_dir)
            sys.path.pop(0)
