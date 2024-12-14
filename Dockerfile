FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1

WORKDIR /server

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r /server/requirements.txt

COPY . /server/

#RUN python3 manage.py migrate
RUN python3 manage.py collectstatic --noinput --clear

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]