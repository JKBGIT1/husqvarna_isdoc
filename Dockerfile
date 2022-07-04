FROM python:slim-bullseye

WORKDIR /my_app

COPY . ./

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "-m" , "flask", "run", "--host=0.0.0.0", "--port=5000"]