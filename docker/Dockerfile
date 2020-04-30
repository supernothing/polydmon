FROM pypy:3.6

WORKDIR /usr/src/app
COPY README.md requirements.txt setup.py ./
COPY src src
RUN pip install .

