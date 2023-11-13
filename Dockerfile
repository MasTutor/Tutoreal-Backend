FROM python:3.10.10

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt 

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8080", "main:app"]
ENTRYPOINT ["streamlit", "run", "doc/doc.py,", "--server.port=8080", "--server.address=0.0.0.0"]
