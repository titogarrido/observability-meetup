# base image
FROM python:3.6.5-slim

# set working directory
WORKDIR /usr/src/app

# add and install requirements
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# add entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# add app
RUN mkdir /usr/src/app/templates
COPY templates/* /usr/src/app/templates
COPY frontend.py /usr/src/app

# run server
CMD ["/usr/src/app/entrypoint.sh"]
