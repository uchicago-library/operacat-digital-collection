FROM python:3.5-alpine
COPY . /code
WORKDIR /code
RUN python setup.py install
ENV ELASTIC_SEARCH_ADDRESS
ENV OPERACAT_SECRET_KEY="changethisinproductionenvironments"
ENV OPERACAT_PROJECT_DIR="/code/"
RUN pip install gunicorn
CMD gunicorn operacat.wsgi
