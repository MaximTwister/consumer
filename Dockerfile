FROM python

COPY ./common /collector/common
COPY ./database /collector/database
COPY requirements.txt /collector
COPY server.py /collector

WORKDIR /collector

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "server.py"]