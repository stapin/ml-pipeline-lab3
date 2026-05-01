FROM alpine:latest
RUN apk add --no-cache ansible

WORKDIR /app
COPY secrets.vault ./

RUN printf "import yaml\n\
with open('/tmp/full_secrets.yml') as f:\n\
    data = yaml.safe_load(f)\n\
with open('/shared/db_pass.txt', 'w') as f:\n\
    f.write(str(data.get('DB_PASSWORD', '')).strip())\n" > extract.py

RUN echo '#!/bin/sh' > decrypt.sh && \
    echo 'echo "$VAULT_PASS" > /tmp/temp_pass.txt' >> decrypt.sh && \
    echo 'ansible-vault decrypt secrets.vault --vault-password-file /tmp/temp_pass.txt --output /tmp/full_secrets.yml' >> decrypt.sh && \
    echo 'python3 extract.py' >> decrypt.sh && \
    echo 'chmod 644 /shared/db_pass.txt' >> decrypt.sh && \
    echo 'rm /tmp/temp_pass.txt /tmp/full_secrets.yml extract.py' >> decrypt.sh && \
    chmod +x decrypt.sh

CMD ["./decrypt.sh"]