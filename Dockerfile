FROM python:latest


WORKDIR /app
COPY . /app
COPY requirements.txt .
RUN pip install -U pip
RUN pip install -r requirements.txt

EXPOSE 8000
ENV NAME FastAPI

CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000"]