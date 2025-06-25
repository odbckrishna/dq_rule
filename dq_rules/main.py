import os
import yaml
import importlib
from dq_rules.engine.rule_engine import RuleEngine

def main(dataset_name: str, output_csv: str):
    # Load YAML template for the dataset
    onboarding_path = os.path.join(os.path.dirname(__file__), 'onboarding', f'{dataset_name}.yml')
    with open(onboarding_path, 'r') as f:
        config = yaml.safe_load(f)
    # Initialize rule engine
    engine = RuleEngine(config)
    # Run validation and output results
    engine.run(output_csv)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run DQ Rule Validation")
    parser.add_argument('--dataset', required=True, help='Dataset name (YAML template name)')
    parser.add_argument('--output', required=True, help='Output CSV file path')
    args = parser.parse_args()
    main(args.dataset, args.output)

