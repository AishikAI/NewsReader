FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8080
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.enableCORS=false"]
