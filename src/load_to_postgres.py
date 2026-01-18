import os
import json
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# DB connection from .env
conn_params = {
    'host': os.getenv('POSTGRES_HOST'),
    'port': os.getenv('POSTGRES_PORT'),
    'dbname': os.getenv('POSTGRES_DB'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD')
}

def create_raw_table():
    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE SCHEMA IF NOT EXISTS raw;
                CREATE TABLE IF NOT EXISTS raw.telegram_messages (
                    message_id BIGINT,
                    channel_name TEXT,
                    message_date TIMESTAMP,
                    message_text TEXT,
                    has_media BOOLEAN,
                    image_path TEXT,
                    views INTEGER,
                    forwards INTEGER
                );
            """)
            conn.commit()

def load_json_to_db(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            for msg in data:
                cur.execute("""
                    INSERT INTO raw.telegram_messages 
                    (message_id, channel_name, message_date, message_text, has_media, image_path, views, forwards)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING;
                """, (
                    msg['message_id'], msg['channel_name'], msg['message_date'], msg['message_text'],
                    msg['has_media'], msg['image_path'], msg['views'], msg['forwards']
                ))
            conn.commit()

if __name__ == '__main__':
    create_raw_table()
    # Walk through data lake and load all JSON
    for root, dirs, files in os.walk('data/raw/telegram_messages'):
        for file in files:
            if file.endswith('.json'):
                load_json_to_db(os.path.join(root, file))
    print("Data loaded to PostgreSQL.")