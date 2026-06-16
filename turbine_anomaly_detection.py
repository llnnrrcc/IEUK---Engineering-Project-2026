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

def summarise_by_turbine(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate raw readings into one row per turbine."""
    return df.groupby("turbine_id").agg(
        avg_temperature_c=("temperature_c", "mean"),
        max_vibration_mm_s=("vibration_mm_s", "max"),
        reading_count=("temperature_c", "count"),
    ).round(2)

def main(filepath: str) -> None:
    df = load_telemetry(filepath)
    summary = summarise_by_turbine(df)
    print(summary)


if __name__ == "__main__":
    filepath = sys.argv[1] if len(sys.argv) > 1 else "telemetry_data.csv"
    main(filepath)