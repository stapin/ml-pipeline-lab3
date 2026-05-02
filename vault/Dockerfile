FROM python:3.9-slim

RUN pip install ansible-vault pyyaml

WORKDIR /app
COPY secrets.vault vault/extract.py ./

CMD ["python", "extract.py"]