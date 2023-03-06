FROM python:3.11-alpine
COPY . /app
WORKDIR /app
RUN pip install .
EXPOSE 8000
CMD ["python", "./main.py"]