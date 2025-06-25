# Data Quality Rule Base Application

This application manages and validates data quality rules across various categories. Rules are onboarded via YAML templates, and results are output as CSV. The API allows triggering rule validation for a dataset.

## Structure
- `dq_rules/categories/`: Rule category modules (Discovery, Anomaly, etc.)
- `dq_rules/onboarding/`: YAML onboarding logic
- `dq_rules/engine/`: Rule engine core
- `dq_rules/api/`: API endpoint

## Requirements
Install dependencies with:

```
pip install -r requirements.txt
```

## How to Run
1. Onboard your dataset and rules as a YAML file in `dq_rules/onboarding/` (e.g., `my_dataset.yml`).
2. Run the API server:

```
uvicorn dq_rules.api.main:app --reload --port 8000
```

Or run the rule engine directly:

```
python dq_rules/main.py --dataset my_dataset --output results.csv
```

- Replace `my_dataset` with your YAML template name (without `.yml`).
- The output CSV will contain rule validation results.
