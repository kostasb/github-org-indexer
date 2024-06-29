FROM python:3.12
RUN mkdir /data
COPY requirements.txt /data/requirements.txt
RUN pip install -r /data/requirements.txt
ENTRYPOINT ["python3","/data/e2etests.py"]