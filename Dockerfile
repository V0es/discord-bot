FROM ubuntu:latest
LABEL maintainer="v0es"
ENV VIRTUAL_ENV=/opt/venv
WORKDIR /usr/local/bin
COPY . .
RUN apt-get update && \
    apt-get install -y python3 && \
    apt-get install -y python3-pip && \
    pip3 install -r requirements.txt && \
    python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
CMD ["python3", "src/main.py"]
