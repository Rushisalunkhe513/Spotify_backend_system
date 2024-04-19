FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . /app/
EXPOSE 5000
ENV db_url="sqlite:///data.db"
CMD ["flask","run","--host","0.0.0.0"]