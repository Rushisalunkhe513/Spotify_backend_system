# lets add base image for application.
FROM python:3.9-slim

# lets create working die inside Docker
WORKDIR /app

# lets copy requirements.txt in docker dir /app
COPY requirements.txt  /app/requirements.txt

# lets copy application code in docker /app/
COPY . /app/

# set ENV variable
ENV PRODUCTION=True
ENV db_url="sqlite:///data.db"

# lets run command to install all dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# EXPOSE port for DOCKER Mapping
EXPOSE 5000

# lets write command to run application
CMD ["flask","run","--host","0.0.0.0"]