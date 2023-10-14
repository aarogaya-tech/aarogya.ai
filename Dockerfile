FROM python:3.10.9
RUN mkdir -p /home/app
WORKDIR /home/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1 

RUN pip install --upgrade pip

COPY . /home/app
RUN pip install -r requirements.txt
EXPOSE 8000

RUN python wave_website/manage.py makemigrations
RUN python wave_website/manage.py migrate

CMD python wave_website/manage.py runserver 0.0.0.0:8000