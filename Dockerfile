FROM ubuntu:latest
LABEL maintainer="v0es"
WORKDIR /usr/local/bin
COPY . .
RUN apt-get update && \
    apt-get install -y python3 && \
    apt-get install -y python3-pip && \
    pip3 install -r requirements.txt

CMD ["python3", "src/main.py"]
