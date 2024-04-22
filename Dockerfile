FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
ENV PRODUCTION=True
ENV DB_URL="sqlite:///dev.db"
COPY . /app/
EXPOSE 5000
CMD ["flask","run","--host","0.0.0.0"]