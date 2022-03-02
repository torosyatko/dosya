FROM python:3.9.9

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV C_FORCE_ROOT 1

WORKDIR /app
RUN pip install -U pip
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY *.py /app/

CMD python main.py