From python:3.12-slim

WORKDIR /app

ENV FLASK_DEBUG=1

COPY . .

RUN pip install -r requirements.txt

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]

