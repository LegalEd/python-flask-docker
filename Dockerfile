FROM python:3.11-alpine
LABEL maintainer="celias@realla.co.uk"
COPY . /app
WORKDIR /app
RUN apk add pwgen && pwgen -H seed > secret
RUN pip install -r requirements.txt
EXPOSE 8080
ENTRYPOINT ["python"]
CMD ["src/app.py"]
