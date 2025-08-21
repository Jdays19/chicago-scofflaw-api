import psycopg2
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv() 

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# Normalizing address
def clean_address(addr):
    return addr.strip().lower() if isinstance(addr, str) else None

# Connecting to db
conn = psycopg2.connect(
    dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
)
cur = conn.cursor()

# Ingesting violations
print("Ingesting violations...")
violations_df = pd.read_csv("data/Building_Violations.csv")
violations_df["ADDRESS"] = violations_df["ADDRESS"].apply(clean_address)
violations_df["VIOLATION DATE"] = pd.to_datetime(violations_df["VIOLATION DATE"])

for _, row in violations_df.iterrows():
    cur.execute(
        """
        INSERT INTO violations (address, violation_date, violation_code, violation_status, violation_description, inspector_comments)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            row["ADDRESS"],
            row["VIOLATION DATE"].date(),
            row["VIOLATION CODE"],
            row["VIOLATION STATUS"],
            row["VIOLATION DESCRIPTION"],
            row["VIOLATION INSPECTOR COMMENTS"],
        ),
    )

# Ingesting scofflaws
print("Ingesting scofflaws...")
scofflaws_df = pd.read_csv("data/Building_Code_Scofflaw_List.csv")
scofflaws_df["ADDRESS"] = scofflaws_df["ADDRESS"].apply(clean_address)
scofflaws_df["OWNER LIST DATE"] = pd.to_datetime(scofflaws_df["OWNER LIST DATE"], errors="coerce")

for _, row in scofflaws_df.iterrows():
    cur.execute(
        """
        INSERT INTO scofflaws (address, court_case_number, owner_list_date)
        VALUES (%s, %s, %s)
        """,
        (
            row["ADDRESS"],
            row["CIRCUIT COURT CASE NUMBER"],
            row["OWNER LIST DATE"].date() if pd.notnull(row["OWNER LIST DATE"]) else None,
        ),
    )

conn.commit()
cur.close()
conn.close()
print("Ingestion complete.")