FROM python:3.11-slim

LABEL maintainer="ALX Academy CTF"
LABEL challenge="03-broken-login"
LABEL description="SQL Injection - panel logowania"

# Minimalne zaleznosci
RUN pip install --no-cache-dir flask==3.0.0

WORKDIR /app
COPY app.py .

# Flaga jako zmienna srodowiskowa - latwa do zmiany w docker-compose
ENV FLAG=ALX{sql1_byp4ss_un10n_s3l3ct}
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

# Uruchom bez trybu debug (wazne w CTF - nie ujawnia stack trace)
CMD ["python", "app.py"]
