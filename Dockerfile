FROM python:3.9
WORKDIR .
COPY requirements.txt /.
RUN pip install --no-cache-dir -r requirements.txt
COPY redis_management.py /.
COPY flask_app.py /.
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "flask_app:app"]