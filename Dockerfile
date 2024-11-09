FROM python:latest

WORKDIR /app
COPY ./* .
CMD ["make"]