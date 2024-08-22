FROM python:3.12
WORKDIR /usr/src/app
COPY . .
RUN apt install make
RUN pip install -r requirements.txt
CMD [ "make", "prod" ]