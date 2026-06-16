"""
AeroGrid Turbine Anomaly Detection
-----------------------------------
Reads turbine sensor telemetry and flags turbines breaching safety
thresholds.

Anomaly rules:
  - Average temperature exceeds 85.0 C
  - Vibration levels spike above 15.0 mm/s (peak reading)
"""

import sys
import pandas as pd

TEMP_THRESHOLD_C = 85.0
VIBRATION_THRESHOLD_MM_S = 15.0

def load_telemetry(filepath: str) -> pd.DataFrame:
    """Load telemetry data from either a CSV or an Excel file."""
    if filepath.lower().endswith((".xlsx", ".xls")):
        return pd.read_excel(filepath)
    return pd.read_csv(filepath)

def main(filepath: str) -> None:
    df = load_telemetry(filepath)
    print(df.head())


if __name__ == "__main__":
    filepath = sys.argv[1] if len(sys.argv) > 1 else "telemetry_data.csv"
    main(filepath)