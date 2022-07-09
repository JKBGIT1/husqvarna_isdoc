FROM python:slim-bullseye

WORKDIR /my_app

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY . ./

EXPOSE 5000

CMD ["python", "-m", "gunicorn", "app:app"]