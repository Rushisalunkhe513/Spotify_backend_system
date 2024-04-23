# base image
FROM python:3.9-slim
# lets add workdir
WORKDIR /app
# now copy requirements.txt
COPY requirements.txt /app/requirements.txt
# lets run command to install dependencies.
RUN pip install --no-cache-dir --upgrade -r requirements.txt
# lets copy code of host into docker dir
COPY . /app/
# lets add env var
ENV PRODUCTION=True
ENV db_url="sqlite:///dev_db"
# expose port from docker
EXPOSE 5000
# lets run commad to run application
CMD ["flask","run","--host","0.0.0.0"]