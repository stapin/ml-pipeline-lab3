import oracledb
from ansible_vault import Vault
import yaml

class OracleDBManager:
    def __init__(self, vault_path: str = "secrets.vault", vault_pass_path: str = "vault_pass.txt"):
        self.secrets = self._load_secrets(vault_path, vault_pass_path)

        self.user = self.secrets.get("DB_USER")
        self.password = self.secrets.get("DB_PASSWORD")
        self.host = self.secrets.get("DB_HOST", "localhost")
        self.port = self.secrets.get("DB_PORT", "1521")
        self.service = self.secrets.get("DB_SERVICE", "FREEPDB1")
        self.dsn = f"{self.host}:{self.port}/{self.service}"

    def _load_secrets(self, vault_path: str, vault_pass_path: str) -> dict:
        try:
            with open(vault_pass_path, 'r') as f:
                vault_pass = f.read().strip()
            
            vault = Vault(vault_pass)
            with open(vault_path, 'r') as f:
                decrypted_data = vault.load(f.read())
                
            return yaml.safe_load(decrypted_data)
        except Exception as e:
            raise RuntimeError(f"Error reading secret storage: {e}")

    def _get_connection(self):
        return oracledb.connect(
            user=self.user,
            password=self.password,
            dsn=self.dsn
        )

    def init_database(self):
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute("""
                        BEGIN
                           EXECUTE IMMEDIATE 'CREATE TABLE predictions (
                               id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                               text_content CLOB,
                               rating NUMBER
                           )';
                        EXCEPTION
                           WHEN OTHERS THEN
                              IF SQLCODE != -955 THEN RAISE; END IF;
                        END;
                    """)
                    conn.commit()
                except oracledb.DatabaseError as e:
                    print(f"Error during database initialization: {e}")

    def save_prediction(self, text_content: str, predicted_rating: float) -> int:
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                out_id = cursor.var(oracledb.NUMBER)
                
                cursor.execute("""
                    INSERT INTO predictions (text_content, rating)
                    VALUES (:1, :2)
                    RETURNING id INTO :3
                """, [text_content, predicted_rating, out_id])
                
                conn.commit()
                
                return int(out_id.getvalue()[0])