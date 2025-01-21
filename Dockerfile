FROM python:3.9

ENV PYTHONUNBUFFERED=1 

WORKDIR /usr/src/app

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "main:app"]
