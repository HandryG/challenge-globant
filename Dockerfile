FROM python:3.9-slim

WORKDIR /challenge-globant


RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

RUN echo "DIRECTORY LISTING START" && ls -la /challenge-globant/ && echo "DIRECTORY LISTING END"

RUN chmod +x entrypoint.sh


EXPOSE 8000


ENTRYPOINT ["./entrypoint.sh"]