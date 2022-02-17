FROM python:3.10.2 AS production

WORKDIR /app

COPY . .

CMD ["python", "main.py"]


FROM production AS test

RUN pip install -r requirements-test.txt

CMD ["python", "-m", "pytest", "test"]