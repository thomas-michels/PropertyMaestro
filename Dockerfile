FROM python:3.10-alpine

WORKDIR .

COPY ./requirements/prod.txt ./requirements.txt

RUN pip install --upgrade pip \
    && pip install --no-cache-dir --upgrade -r /requirements.txt

COPY ./app ./app
COPY ./run_server.py ./run_server.py

ENTRYPOINT ["python"]

CMD ["run_server.py"]
