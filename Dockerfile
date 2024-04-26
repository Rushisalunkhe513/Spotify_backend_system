# lets get base image
FROM python:3.9-slim

# lets create workdir
WORKDIR /app

# lets copy requirements.txt inside the /app/requirements.txt
COPY requirements.txt /app/requirements.txt

# now lets copy app code into docker dir
COPY . /app/

# lets add env var
ENV PRODUCTION=True
ENV db_url="sqlite://dev.db"

# lets run commad to install dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# lets expose docker port
EXPOSE 5000

# write command to run application
CMD ["flask","run","--host","0.0.0.0"]