FROM python:3.8

RUN apt-get update -y && apt-get install -y python3-pip python3-dev 
RUN pip3 install --upgrade pip

RUN mkdir -p /aura && \
    chmod 777 /aura 

COPY ./requirements.txt /aura/

RUN python3 -m pip install -r /aura/requirements.txt

COPY ./ /aura/
WORKDIR /aura/

#RUN useradd app
#USER app

CMD python3 -u /aura/aura_ml_trainer.py


