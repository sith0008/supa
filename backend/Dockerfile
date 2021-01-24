FROM python:3.8
WORKDIR /backend
ADD . /backend
RUN apt-get update
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["run.py"]
