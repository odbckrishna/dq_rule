import pandas as pd
from typing import List, Dict, Any

def save_rule_results(results: List[Dict[str, Any]], output_csv: str):
    """
    Save rule validation results to a CSV file.
    Args:
        results: List of dictionaries with rule results.
        output_csv: Path to output CSV file.
    """
    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False)
