FROM fedora:latest

# RUN apt-get update && apt install -y curl python3.9
RUN dnf -y update && dnf install -y curl python3.9 yosys
RUN python3.9 -m ensurepip

WORKDIR /bin
RUN curl https://zyedidia.github.io/eget.sh | sh
RUN eget llvm/circt -t firtool-1.44.0
RUN eget zachjs/sv2v -t v0.0.10

WORKDIR /home

COPY requirements.txt .
RUN python3.9 -m pip install -r requirements.txt

COPY *.sv ./
COPY *.sh ./

ENV USE_FIRRTL true

CMD ["./run.sh"]
