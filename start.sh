#!/bin/bash
read -s -p "Enter Vault Password: " VAULT_PASS
echo ""
echo $VAULT_PASS > vault_pass.txt

echo "Starting infrastructure..."
docker run --rm \
  -u root --privileged \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v "$(pwd)":"$(pwd)" -w "$(pwd)" \
  docker:cli \
  sh -c "apk add --no-cache docker-cli-compose ansible && ansible-playbook deploy.yml --vault-password-file vault_pass.txt"
  
echo "Done! Application is running."