FROM arm64v8/alpine
LABEL maintainer="v0es"
WORKDIR /app
COPY . .
RUN apk update && \
    apk add bash && \
    apk add python3
    #apk add py-pip && \
    #pip install -r requirements.txt && \
    #rm -rf /var/cache/apk/*
CMD ["python", "src/main.py"]
