FROM mambaorg/micromamba:latest

EXPOSE 8000

COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yml /tmp/environment.yml
RUN micromamba create --yes --file /tmp/environment.yml && \
    micromamba clean --all --yes

ARG MAMBA_DOCKERFILE_ACTIVATE=1

ENV ENV_NAME csv-tool

WORKDIR /opt
COPY ./src /opt

CMD uvicorn main:app --host 0.0.0.0 --port 8000

