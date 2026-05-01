import oracledb
import os


class OracleDBManager:
    def __init__(self):
        with open("/run/secrets/db_pass.txt", "r") as f:
            self.password = f.read().strip()
        self.user = os.getenv("DB_USER")
        self.host = os.getenv("DB_HOST", "localhost")
        self.port = os.getenv("DB_PORT", "1521")
        self.service = os.getenv("DB_SERVICE", "FREEPDB1")
        self.dsn = f"{self.host}:{self.port}/{self.service}"

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