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

def flag_anomalies(summary: pd.DataFrame) -> pd.DataFrame:
    """Mark turbines that breach either the temperature or vibration rule."""
    summary["temp_anomaly"] = summary["avg_temperature_c"] > TEMP_THRESHOLD_C
    summary["vibration_anomaly"] = summary["max_vibration_mm_s"] > VIBRATION_THRESHOLD_MM_S
    summary["requires_maintenance"] = summary["temp_anomaly"] | summary["vibration_anomaly"]
    return summary

def main(filepath: str) -> None:
    try:
        df = load_telemetry(filepath)
    except FileNotFoundError:
        print(f"Error: could not find a file at '{filepath}'. Check the path and try again.")
        sys.exit(1)
    except (ValueError, UnicodeDecodeError):
        print(f"Error: '{filepath}' could not be read as a CSV or Excel file.")
        sys.exit(1)

    required_columns = {"turbine_id", "temperature_c", "vibration_mm_s"}
    missing = required_columns - set(df.columns)
    if missing:
        print(f"Error: the data is missing required column(s): {', '.join(missing)}")
        sys.exit(1)

    summary = flag_anomalies(summarise_by_turbine(df))

    print("Turbine Health Summary")
    print(summary.to_string())
    print()

    failing = summary[summary["requires_maintenance"]]
    if failing.empty:
        print("No turbines are currently breaching the anomaly thresholds.")
        return
    
    print(f"URGENT MAINTENANCE REQUIRED: {len(failing)} turbine(s) flagged")
    for turbine_id, row in failing.iterrows():
        reasons = []
        if row["temp_anomaly"]:
            reasons.append(f"avg temp {row['avg_temperature_c']}C exceeds {TEMP_THRESHOLD_C}C")
        if row["vibration_anomaly"]:
            reasons.append(f"peak vibration {row['max_vibration_mm_s']}mm/s exceeds {VIBRATION_THRESHOLD_MM_S}mm/s")
        print(f"  - {turbine_id}: {', '.join(reasons)}")



    


if __name__ == "__main__":
    filepath = sys.argv[1] if len(sys.argv) > 1 else "telemetry_data.csv"
    main(filepath)