FROM python:3.11
LABEL maintainer="celias@realla.co.uk"
COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
EXPOSE 8080
WORKDIR /app/src
ENTRYPOINT ["python", "-m", "flask", "--debug", "run", "--host=0.0.0.0"]
