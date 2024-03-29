FROM python:3.9.19-slim
WORKDIR /src
COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn eventlet gevent
RUN pip install tornado
RUN pip install markupsafe
COPY . .
# CMD ["gunicorn", "-b", "0.0.0.0:8000", "main:app"]
CMD ["gunicorn", "-b", "0.0.0.0:8000", "-w", "4", "-k", "eventlet", "--timeout", "60", "main:app"]
# CMD ["python", "main.py"]
### different -k sync, eventlet, gevent, tornado, gthread