FROM python:3.12.1-alpine3.19

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV SERVER_PORT=8000

CMD ["sh" , "-c", "alembic upgrade head && python -m uvicorn src.main:app --host=0.0.0.0 --port=$SERVER_PORT"]
