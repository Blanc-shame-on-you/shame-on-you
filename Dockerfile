FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y git

RUN mkdir /shame-on-you
WORKDIR /shame-on-you

## install packages
RUN pip install -r requirements.txt

ADD . /shame-on-you/

## Run the application on the port 8080
EXPOSE 8000 

#CMD ["python", "./setup.py", "runserver", "--host=0.0.0.0", "-p 8080"] 
CMD python3 webstreaming.py