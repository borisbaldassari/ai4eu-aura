FROM python:3.8

RUN apt-get update -y && apt-get install -y python3-pip python3-dev 
RUN pip3 install --upgrade pip
#RUN pip3 install -r requirements.txt

RUN mkdir /scripts/ /data_in/ /data_out/
COPY scripts/ /scripts/
WORKDIR /scripts/

RUN useradd app
USER app

ENTRYPOINT ["/scripts/aura_clean_process_dir.sh", "-i", "/data_in", "-o", "/data_out"]


