# Derivando da imagem oficial do Python 3.9
FROM python:3.10-slim-bookworm as builder

# WORKDIR /mysqlclient-python

# reference from : https://github.com/PyMySQL/mysqlclient#linux
RUN apt update && \
    apt install -y python3-dev default-libmysqlclient-dev build-essential pkg-config

# copy libmariadb to /libmariadb
RUN mkdir -p /libmariadb && \
    cp -r /usr/lib/x86_64-linux-gnu/libmariadb* /libmariadb

# copy mysqlclient package to /mysqlclient
RUN mkdir -p /mysqlclient && \
    pip wheel mysqlclient==2.2.0 --wheel-dir=/mysqlclient
# cp -r /usr/local/lib/python3.10/site-packages/mysqlclient-2.2.0.dist-info /mysqlclient/mysqlclient-2.2.0.dist-info  && \
#     cp -r /usr/local/lib/python3.10/site-packages/MySQLdb /mysqlclient/MySQLdb

# ===================================================================================================
# stage 2 - install mysqlclient from wheel
FROM python:3.10-slim-bookworm as runner

# copy and install wheel from stage 1
COPY --from=builder /mysqlclient /mysqlclient
COPY --from=builder /libmariadb /usr/lib/x86_64-linux-gnu

RUN pip install --no-index --find-links=/mysqlclient mysqlclient

WORKDIR /app

# Set locale
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV LANGUAGE=C.UTF-8

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

ENV TZ="Asia/Taipei"
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

COPY . .

# Mover o arquivo de dependência do projeto para a pasta code
COPY ./requirements.txt .

RUN  pip install --no-cache-dir --upgrade -r requirements.txt

# Comando para subir o app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]