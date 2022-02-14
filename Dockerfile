FROM python:3.8.11-slim-buster AS build_base

# install dependent packages
RUN apt-get -y update && apt-get install -y --no-install-recommends \
  # for install
  curl \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*# install poetry

WORKDIR /home
ENV HOME /home
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH $PATH:/home/.poetry/bin
RUN poetry config virtualenvs.create false

WORKDIR /app
COPY . /app

RUN poetry install --no-dev

FROM build_base AS test_runner
# install full dependencies (includes dev-dependencies)
RUN poetry install
