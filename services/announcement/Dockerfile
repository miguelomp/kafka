FROM python:3.10.5 AS BUILDER

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

FROM python:3.10.5-slim-buster AS IMAGE
COPY --from=BUILDER /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app
COPY ./src .

CMD faust -A main worker -l info
