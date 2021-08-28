FROM python:3.9

EXPOSE 8000


COPY ./requirements.txt /requirements.txt

RUN pip install -r requirements.txt
COPY ./app /app


WORKDIR /app

CMD ["uvicorn", "--reload", "--host", "0.0.0.0", "--port", "8000", "main:app"]
