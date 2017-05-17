FROM python:3.5
COPY . /code
WORKDIR /code
RUN apt-get update &&\
  apt-get install -y libjpeg-dev zlib1g-dev &&\
  apt-get clean
RUN python setup.py install
ENV ELASTIC_SEARCH_ADDRESS=""
ENV OPERACAT_BASE_URL=""
ENV OPERACAT_SECRET_KEY="changethisinproductionenvironments"
ENV OPERACAT_PROJECT_DIR="/code/"
RUN pip install gunicorn
CMD gunicorn operacat.wsgi -b 0.0.0.0:8000
