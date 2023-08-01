FROM python

WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "./app.py"]
#ENTRYPOINT FLASK_APP=/opt/app.py flask run --host=0.0.0.0 --port=5000

