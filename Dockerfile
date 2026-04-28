FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

WORKDIR /code/TankYouProj

RUN adduser --disabled-password --gecos '' django_user
RUN chown -R django_user:django_user /code

USER django_user

CMD ["gunicorn", "TankYou.wsgi:application", "--bind", "0.0.0.0:8000"]
