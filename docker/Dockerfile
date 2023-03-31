FROM python:3.11-slim

RUN groupadd -g 1000 app && \
    useradd --system --create-home --home-dir /app -s /bin/bash -g app -u 1000 app
WORKDIR /app

LABEL project = 'astraeus'
LABEL component = 'edsm-reader'

RUN apt-get update && \
    apt-get install -y make git gcc iputils-ping wget libpq-dev && \
    pip install -U pip && \
    rm -rf /var/lib/apt/lists/*

USER 1000

WORKDIR /app
COPY --chown=app dist/edsm_reader-*.whl .
COPY --chown=app docker/entrypoint.sh .

RUN chmod +x /app/entrypoint.sh

RUN pip install edsm_reader-*.whl

USER root
RUN apt-get remove -y --purge gcc && \
    apt autoremove -y && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /tmp/wheels && \
    rm -rf edsm_reader-*.whl

USER 1000

WORKDIR /app

ENTRYPOINT [ "/app/entrypoint.sh" ]
CMD [ "python", "-m", "edsm_reader", "--log_level", "INFO" ]
