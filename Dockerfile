FROM ubuntu:16.04

RUN adduser flask --disabled-password --disabled-login
RUN apt-get update && apt-get -y install python3 python3-pip python3-venv git virtualenv

COPY . /app
# Clean previous virtualenv
WORKDIR /app
RUN if [ -e venv ]; then rm -rf venv; fi

RUN chown -R flask:flask /app

USER flask

RUN python3 -m venv venv
RUN ./venv/bin/pip install --upgrade pip
RUN ./venv/bin/pip install -r requirements.txt
ENV FLASK_APP run.py
EXPOSE 5000

#CMD ["/bin/bash"]
ENTRYPOINT ["/bin/bash", "-c", "source ./init_environment.sh; ./boot.sh"]
