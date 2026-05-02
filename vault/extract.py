import sys
from ansible_vault import Vault

try:
    with open('/run/secrets/vault_password', 'r') as f:
        password = f.read().strip()
except FileNotFoundError:
    print("Error: Secrets not found!")
    sys.exit(1)

vault = Vault(password)
try:
    with open('secrets.vault', 'r') as f:
        data = vault.load(f.read())
except Exception as e:
    print(f"Decrypt error: {e}")
    sys.exit(1)

with open('/shared/db_pass.txt', 'w') as f:
    f.write(str(data.get('DB_PASSWORD', '')).strip())

print("Success: Secrets saved.")