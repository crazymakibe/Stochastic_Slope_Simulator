
FROM python:3.10-slim


RUN apt-get update && apt-get install -y \
    libgdal-dev \
    g++ \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


RUN mkdir src


CMD ["tail", "-f", "/dev/null"]
