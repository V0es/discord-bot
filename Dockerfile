FROM arm64v8/alpine
LABEL maintainer="v0es"
WORKDIR /usr/local/bin
COPY . .
RUN apk update && \
    apk add --no-cache bash && \
    apk install -y python3 && \
    apk install -y python3-pip && \
    pip3 install -r requirements.txt

CMD ["python3", "src/main.py"]
