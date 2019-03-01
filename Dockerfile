FROM python:3.6
ENV PYTHONUNBUFFERED 1
ENV C_FORCE_ROOT true
ENV DJANGO_SECRET_KEY=dont-tell-eve
RUN mkdir /src
RUN mkdir /static
WORKDIR /src
COPY ./system_test_progress_tracking /src
COPY ./requirements.txt /src
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD python manage.py migrate; python manage.py runserver 0.0.0.0:8000