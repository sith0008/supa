# TODO: add dockerfile configs for ingestion

FROM python:3.8
WORKDIR /ingestion
ADD . /ingestion
RUN apt-get update
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["run.py"]