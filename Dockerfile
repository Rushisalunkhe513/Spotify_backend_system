# base image for application
FROM python:3.9-slim

# now add workdir
WORKDIR /app

# now lets copy requirements.txt intp app
COPY requirements.txt /app/requirements.txt

# now lets COPY application code into workdir
COPY . /app/

# now RUN and Install dependecies.
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# now add env var
ENV PRODUCTION=True
ENV db_url="sqlite:///dev.db"

# noe expose docker port
EXPOSE 5000

# command to run pplication
CMD ["flask","run","--host","0.0.0.0"]