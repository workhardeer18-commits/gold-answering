FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install -i https://mirror2.chabokan.net/pypi/simple/ --upgrade pip
RUN pip install -i https://mirror2.chabokan.net/pypi/simple/ -r requirements.txt

COPY . .

RUN chmod +x /app/deploy.sh
