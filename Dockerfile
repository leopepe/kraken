FROM iron/python:3

COPY credentials /root/.aws/
RUN chmod 600 ~/.aws/credentials
COPY ./kraken /app/kraken
COPY ./packages /app/packages
ENV PYTHONPATH /app/packages
WORKDIR /app
ENTRYPOINT ["python3", "-m", "kraken"]

