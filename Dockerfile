# lets choose base image for application
FROM python:3.9-slim

# lets create working dir in docker
WORKDIR /app

# lets copy requirements.txt to docker /app/requirements.txt
COPY requirements.txt /app/requirements.txt

# lets copy application code to docker dir
COPY . /app/

# lets run command to install requirements.txt dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# now lets get env var
ENV PRODUCTION=True
ENV db_url=sqlite:///dev.db

# lets expose docker port
EXPOSE 5000

# lets write a command to run flask application
CMD ["flask","run","--host","0.0.0.0"]