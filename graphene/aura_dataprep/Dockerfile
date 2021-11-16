FROM python:3.8

RUN apt-get update -y && apt-get install -y python3-pip python3-dev 
#RUN pip3 install --upgrade pip

RUN mkdir -p /aura && \
    chmod 777 /aura 
    
#    mkdir -p /data_out/data/ && \
#    chmod 777 /data_out/data/
#    mkdir -p /data_in && \
#    chmod 777 /data_in && \

COPY ./requirements.txt /aura/

RUN python3 -m pip install -r /aura/requirements.txt

COPY ./ /aura/
WORKDIR /aura/

#RUN useradd -m app
#USER app

RUN ls -al /aura/*

CMD python3 -u /aura/aura_dataprep.py
#ENTRYPOINT ["/scripts/aura_dataprep.sh", "-i", "/data_in", "-o", "/data_out"]
#ENTRYPOINT python3 -u aura_dataprep.py
