FROM python:3.11
LABEL maintainer="celias@realla.co.uk"


RUN apt-get update && \
	apt-get install --no-install-recommends -y unzip wget make libmagic1 libcurl4 w3m imagemagick poppler-utils && \
	rm -rf /var/lib/apt/lists/*


COPY . /app
WORKDIR /app

ENV PIP_NO_CACHE_DIR=off \
	PIP_DISABLE_PIP_VERSION_CHECK=on \
	PIP_DEFAULT_TIMEOUT=100 \
	PYTHONDONTWRITEBYTECODE=1 \
	POETRY_VERSION=1.6.1

# poetry install requirements
ADD pyproject.toml poetry.lock /tmp/
RUN cd /tmp && \
	python -m venv poetry-install && \
	poetry-install/bin/pip install "poetry==$POETRY_VERSION" && \
	poetry-install/bin/poetry export --without-hashes -f requirements.txt -o requirements.txt && \
	printf "pyod==0.9.8\n" >> requirements.txt && \
	rm -rf poetry-install && \
	pip install -r /tmp/requirements.txt --no-deps && \
	cd /usr/local/lib/python3.11/site-packages && \
	find -name \*.pyc -delete && \
	find -name tests -prune -exec rm -r \{\} \; && \
	find -name __pycache__ -prune -exec rm -r \{\} \; && \
	rm -rf ~/.local/share /tmp/requirements.txt


EXPOSE 8081
WORKDIR /app/src
ENTRYPOINT ["/bin/bash", "-c", "python -m flask run --host=0.0.0.0 --port=8081"]
