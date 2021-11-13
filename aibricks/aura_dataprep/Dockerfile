FROM python:3.8

RUN apt-get update -y && apt-get install -y python3-pip python3-dev 
#RUN pip3 install --upgrade pip

RUN mkdir -p /aura 
COPY . /aura/
WORKDIR /aura/

RUN python3 -m pip install -r requirements.txt

RUN useradd -m app
USER app

RUN ls -al /aura/*

CMD python3 -u /aura/aura_dataprep.py
#ENTRYPOINT ["/scripts/aura_dataprep.sh", "-i", "/data_in", "-o", "/data_out"]
#ENTRYPOINT python3 -u aura_dataprep.py
