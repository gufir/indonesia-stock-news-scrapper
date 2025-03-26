# Gunakan image Python sebagai base
FROM python:3.11

RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/*

RUN echo "id_ID.UTF-8 UTF-8" >> /etc/locale.gen && locale-gen

ENV LANG=id_ID.UTF-8
ENV LANGUAGE=id_ID:en
ENV LC_ALL=id_ID.UTF-8

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "api.py"]
