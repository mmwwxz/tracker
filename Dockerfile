# Указывает Docker использовать официальный образ python 3 с dockerhub в качестве базового образа
FROM python:3.10
# Устанавливает переменную окружения, которая гарантирует, что вывод из python будет отправлен прямо в терминал без предварительной буферизации
ENV PYTHONIOENCODING UTF-8
ENV PYTHONUNBUFFERED 1
ENV TZ=ASIA/Bishkek
WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY nginx/nginx.conf /etc/nginx/conf.d/

COPY . /app/

RUN python manage.py makemigrations && \
    python manage.py migrate && \
    python manage.py collectstatic --noinput \
