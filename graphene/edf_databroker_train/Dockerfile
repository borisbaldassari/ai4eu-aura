FROM python:3.8

RUN apt-get update -y && apt-get install -y python3-pip python3-dev 
RUN pip3 install --upgrade pip

RUN mkdir -p /edf_databroker && \
    chmod 777 /edf_databroker
    
COPY ./requirements.txt /edf_databroker/

RUN python3 -m pip install -r /edf_databroker/requirements.txt

COPY ./ /edf_databroker/
WORKDIR /edf_databroker

# RUN useradd app
# USER app

CMD python3 -u edf_databroker_train.py
#ENTRYPOINT python3 -u edf_databroker_train.py

