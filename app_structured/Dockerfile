FROM debian:bullseye-slim

RUN apt-get update && apt-get install -y \
    wget \
    gnupg2 \
    curl \
    lsb-release \
    python3 \
    python3-pip \
    bash \
    && apt-get clean

RUN wget -qO - https://packages.fluentbit.io/fluentbit.key | apt-key add -
RUN echo "deb https://packages.fluentbit.io/debian/$(lsb_release -cs) $(lsb_release -cs) main" > /etc/apt/sources.list.d/fluent-bit.list

RUN mkdir -p /fluent-bit/etc /fluent-bit/python-scripts
COPY fluent-bit.conf /fluent-bit/etc/
COPY parsers.conf /fluent-bit/etc/

RUN apt-get update && apt-get install -y fluent-bit

COPY fluent-bit.conf /fluent-bit/etc/fluent-bit.conf
COPY parsers.conf /fluent-bit/etc/parsers.conf
COPY app_structured.py /fluent-bit/python-scripts/app_structured.py

CMD ["/opt/fluent-bit/bin/fluent-bit", "-c", "/fluent-bit/etc/fluent-bit.conf"]
