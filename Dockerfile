FROM python:3.13-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml .

RUN uv sync

# from less frequently changed to most:
COPY catchup.py .

COPY elt_tobronze.py .

COPY elt_tosilver.py .

COPY elt_togold.py .

COPY export_streamlit.py .

COPY pipeline_prefect.py .

# copy the dbt directory with models and macros
COPY rental_dbt/ .
