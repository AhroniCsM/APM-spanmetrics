FROM python:3.11-slim

WORKDIR /app

ENV DD_ENV="production" \
    DD_SERVICE="service-t-datadog" \
    DD_TRACE_ENABLED=true \
    DD_PROFILING_ENABLED=true \
    DD_RUNTIME_METRICS_ENABLED=true

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5004

CMD ["python", "app.py"]