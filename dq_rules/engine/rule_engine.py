import os
import glob
import importlib
import pandas as pd

class RuleEngine:
    def __init__(self, config):
        self.config = config
        self.dataset_name = config.get('dataset_name')
        self.rules = config.get('rules', {})
        self.data_path = config.get('data_path')
        self.category_modules = {}

    def load_data(self):
        # For demo, assume CSV. Extend for other formats as needed.
        return pd.read_csv(self.data_path)

    def run(self, output_csv):
        data = self.load_data()
        results = []
        for col, col_rules in self.rules.items():
            for rule in col_rules:
                category = rule['category']
                rule_name = rule['name']
                params = rule.get('params', {})
                # Dynamically import category module
                if category not in self.category_modules:
                    mod = importlib.import_module(f'dq_rules.categories.{category}')
                    self.category_modules[category] = mod
                else:
                    mod = self.category_modules[category]
                rule_func = getattr(mod, rule_name)
                # For anomaly rules, pass the match_col series if needed
                if category == 'anomaly' and 'match_col' in params:
                    match_col = params['match_col']
                    params_no_match = {k: v for k, v in params.items() if k != 'match_col'}
                    # Ensure match_col is not None and is a string
                    if match_col and isinstance(match_col, str) and match_col in data.columns:
                        try:
                            passed, obs = rule_func(data[col], **params_no_match, **{match_col: data[match_col]})
                        except Exception as e:
                            passed, obs = False, f"Error in anomaly rule: {e}"
                    else:
                        try:
                            passed, obs = rule_func(data[col], **params_no_match)
                        except Exception as e:
                            passed, obs = False, f"Error in anomaly rule: {e}"
                else:
                    try:
                        passed, obs = rule_func(data[col], **params)
                    except Exception as e:
                        passed, obs = False, f"Error in rule: {e}"
                results.append({
                    'column': col,
                    'rule': rule_name,
                    'category': category,
                    'passed': passed,
                    'observation': obs
                })
        pd.DataFrame(results).to_csv(output_csv, index=False)
