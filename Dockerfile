# adding base image for container
FROM python:3.9-slim

# lets make dir in docker
WORKDIR /app

# lets copy requirements.txt in /app/requiremnts.txt
COPY requirements.txt /app/requirements.txt

# now lets give env var
ENV PRODUCTION=True
ENV db_url="sqlite:///dev.db"

# copy app code in docker dir
COPY . /app/

# lets run command to  install all dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# lets expose docker port
EXPOSE 5000

# lets write command to run application
CMD ["flask","run","--host","0.0.0.0"]
