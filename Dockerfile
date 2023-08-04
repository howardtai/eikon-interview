FROM python:3.9

WORKDIR /app
COPY ./requirements.txt /app/
RUN pip install -r /app/requirements.txt


CMD ["python", "api/api.py"]