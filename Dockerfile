FROM python:3.9
WORKDIR .
COPY requirements.txt /.
RUN pip install --no-cache-dir -r requirements.txt
COPY .env /.
COPY redis_management.py /.
COPY flask_app.py /.
CMD python flask_app.py 
