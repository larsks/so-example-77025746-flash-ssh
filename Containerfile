FROM python:3.11-slim-bullseye

# update/install necessary alpine linux libraries
RUN apt-get -y update
RUN apt-get install -y openssh-client

RUN pip install pipenv

# create project directory
WORKDIR /app
COPY requirements.txt ./
RUN pipenv install -r requirements.txt
COPY . ./
RUN mkdir -m 700 -p /root/.ssh && cp ssh_config /root/.ssh/config && chmod 600 /root/.ssh/config

ENV SSH_AUTH_SOCK=/tmp/agent.sock

CMD ["ssh-agent", "-a", "/tmp/agent.sock", "pipenv", "run", "flask", \
	"--app", "app", "run", "--host", "0.0.0.0", "--port", "5000"]

