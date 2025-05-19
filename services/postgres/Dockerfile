FROM postgis/postgis:latest
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      less \
      make \
      vim \
      git \
      gcc \
      postgresql-server-dev-17 \
 && rm -rf /var/lib/apt/lists/*

RUN cd /tmp \
 && git clone https://github.com/postgrespro/rum \
 && cd rum \
 && make USE_PGXS=1 \
 && make USE_PGXS=1 install

WORKDIR /tmp/db
COPY schema.sql /docker-entrypoint-initdb.d/01_schema.sql
