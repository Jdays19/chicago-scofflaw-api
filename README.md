# Chicago Scofflaw API

#### Back-end service that ingests two City of Chicago datasets, joins them by **address**, and exposes three endpoints.

**Stack:**
- Python 
- Flask 
- PostgreSQL 
- pandas 
- python-dotenv

---

#### Requirements
- Flask
- psycopg2-binary
- python-dotenv
- pandas

```bash
# Install requirements
pip install -r requirements.txt
```
---

#### Project Structure
- api/
    - app.py
- data/
    - Building_Code_Scofflaw_List.csv
    - Building_Violations.csv
- docs/
    - api_documentation.md
- ingestion/
    - ingest_data.py
- sql/
    - create_index.sql
    - create_tables.sql
- tests/
    - test_data.py

---

### Quick Start

**1) Start the Python env**
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```
**2) .env (created in repo root)**
Includes name, username, password, location, and port of DB:
```
- DB_NAME=scofflaw_db    
- DB_USER=scofflaw_user
- DB_PASS=scofflaw_pass
- DB_HOST=localhost
- DB_PORT=5432
```

**3) PostgreSQL (in psql)**
```sql
CREATE DATABASE scofflaw_db;
CREATE USER scofflaw_user WITH PASSWORD 'scofflaw_pass';
GRANT ALL PRIVILEGES ON DATABASE scofflaw_db TO scofflaw_user;
```

**4) Tables + Indexes**
```bash
psql -U scofflaw_user -d scofflaw_db -f sql/create_tables.sql
psql -U scofflaw_user -d scofflaw_db -f sql/create_indexes.sql
```

**5) Ingest CSVs**
```bash
python ingestion/ingest_data.py
```

**6) Run API**
```bash
python api/app.py
```

### open: http://127.0.0.1:5000/

---

### Testing Purposes
Displays first 10 addresses. 
```python
import pandas as pd

violations_df = pd.read_csv("data/Building_Violations.csv")
print(violations_df["ADDRESS"].head(10))
```

Open a new terminal while the server is running.
```bash
# Run to locate violations for the given property
curl http://127.0.0.1:5000/property/7120%20S%20ROCKWELL%20ST/
```
Output returned in JSON format.

---
### Additonal Notes

**Tables:**
- violations
- scofflaws
- comments

**Includes JSON error handlers for:**
- 400
- 404
- 405