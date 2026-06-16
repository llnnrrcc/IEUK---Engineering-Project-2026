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


def main(filepath: str) -> None:
    pass


if __name__ == "__main__":
    filepath = sys.argv[1] if len(sys.argv) > 1 else "telemetry_data.csv"
    main(filepath)