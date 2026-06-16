FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY turbine_anomaly_detection.py .

ENTRYPOINT ["python", "turbine_anomaly_detection.py"]
CMD ["telemetry_data.csv"]