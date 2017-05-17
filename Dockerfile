FROM python:3.5
COPY . /code
WORKDIR /code
RUN apt-get update &&\
  apt-get install -y libjpeg-dev zlib1g-dev &&\
  apt-get clean
RUN python setup.py install
ARG ELASTIC_SEARCH_ADDRESS
ENV ELASTIC_SEARCH_ADDRESS=$ELASTIC_SEARCH_ADDRESS
ARG OPERACAT_BASE_URL
ENV OPERACAT_BASE_URL=$OPERA_CAT_BASE_URL
ARG OPERACAT_SECRET_KEY="changethisinproductionenvironments"
ENV OPERACAT_SECRET_KEY=$OPERACAT_SECRET_KEY
ENV OPERACAT_PROJECT_DIR="/code/"
RUN pip install gunicorn
CMD gunicorn operacat.wsgi -b 0.0.0.0:8000
