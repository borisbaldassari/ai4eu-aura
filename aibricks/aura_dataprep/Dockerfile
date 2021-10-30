FROM python:3.8

RUN apt-get update -y && apt-get install -y python3-pip python3-dev 
#RUN pip3 install --upgrade pip

RUN mkdir /aura_dataprep /scripts/ /data/
COPY . /aura_dataprep
WORKDIR /aura_dataprep/

RUN pip3 install -r requirements.txt

RUN useradd app
USER app

RUN ls -al /data/

ENTRYPOINT python3 -u aura_dataprep.py
#ENTRYPOINT ["/scripts/aura_clean_process_dir.sh", "-i", "/data_in", "-o", "/data_out"]

