FROM python:3.11-slim
RUN apt update && \
    apt-get install -y curl build-essential libatlas-base-dev liblapack-dev
RUN mkdir -p /home/mosef
WORKDIR /home/mosef
COPY . .
RUN bash ./install.sh
RUN python3 -m pip install -r requirements.txt
CMD bash -c "cd bin && . run.sh"

