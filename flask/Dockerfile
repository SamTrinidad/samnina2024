
FROM --platform=$BUILDPLATFORM python:3.12.1-alpine3.18 AS builder

WORKDIR /src
COPY requirements.txt /src
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

COPY . .

CMD ["python", "server.py"]

FROM builder as dev-envs

RUN apk update
RUN apk add git
RUN addgroup -S docker
RUN adduser -S --shell /bin/bash --ingroup docker vscode

# install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / /

CMD ["python", "server.py"]
