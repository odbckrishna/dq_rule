"""
Sample script to execute dq_rules.main using sample_data.csv and sample_dataset.yml.
This will generate results_sample.csv with rule validation results.
"""
import os
import subprocess
import sys
import yaml

if __name__ == "__main__":
    # Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset = "book_data"
    output_csv = os.path.join(base_dir, "results_book_data.csv")
    # Use the current Python executable (virtual environment)
    python_exe = sys.executable
    # Ensure the workspace root is in PYTHONPATH for dq_rules imports
    env = os.environ.copy()
    env["PYTHONPATH"] = base_dir + os.pathsep + env.get("PYTHONPATH", "")
    # No patching needed for book_data, as its YAML is already correct
    # Run the main.py script
    subprocess.run([
        python_exe, os.path.join(base_dir, "dq_rules", "main.py"),
        "--dataset", dataset,
        "--output", output_csv
    ], check=True, env=env)
    print(f"Results written to {output_csv}")

