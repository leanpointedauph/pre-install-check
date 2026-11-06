FROM python:3.12-slim
WORKDIR /app
COPY paywall.py app.py checker.py ./
ENV PAYWALL_DB=/tmp/paywall.sqlite
CMD ["python", "app.py"]
