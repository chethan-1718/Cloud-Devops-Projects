FROM jenkins/inbound-agent:latest

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       curl ca-certificates git python3 python3-pip python3-venv \
    && install -d -m 0755 /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/debian/gpg \
       -o /etc/apt/keyrings/docker.asc \
    && chmod a+r /etc/apt/keyrings/docker.asc \
    && . /etc/os-release \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian ${VERSION_CODENAME} stable" \
       > /etc/apt/sources.list.d/docker.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends docker-ce-cli docker-compose-plugin \
    && if ! getent group 1001 >/dev/null; then groupadd -g 1001 docker-host; fi \
    && usermod -aG "$(getent group 1001 | cut -d: -f1)" jenkins \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER jenkins