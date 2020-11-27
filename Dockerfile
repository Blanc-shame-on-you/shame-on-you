FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-venv

RUN mkdir /shame-on-you
RUN cd /shame-on-you
WORKDIR /shame-on-you

## install packages
RUN python3 -m venv venv
RUN source venv/bin/activate
RUN pip install -r requirements.txt

ADD . /shame-on-you/

## Run the application on the port 8080
EXPOSE 5000

#CMD ["python", "./setup.py", "runserver", "--host=0.0.0.0", "-p 8080"] 
CMD ["python3", "webstreaming.py"]