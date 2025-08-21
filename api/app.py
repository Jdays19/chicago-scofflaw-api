from flask import Flask, request, jsonify, abort
import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()   # loading environment variables 

app = Flask(__name__)

# DB config -- read from environment to prevent hardcoding credentials
DB_NAME = os.getenv("DB_NAME")  # .env file
DB_USER = os.getenv("DB_USER")  # .env file
DB_PASS = os.getenv("DB_PASS")  # .env file
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")  # default port 

# Opens new Postgres connection
def get_db_connection():
    return psycopg2.connect(
        dbname=DB_NAME, 
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )

# Maps to route url -- ensures its running
@app.route('/')
def home():
    return 'API is currently running.' 

# API endpoint #1: Locates a property by address
@app.route('/property/<path:address>/', methods=['GET'])
def get_property(address):
    address_clean = address.strip().lower() # normalize so joins function properly
    conn = get_db_connection()
    cur = conn.cursor()

    # Gets violations
    cur.execute("""
        SELECT violation_date, violation_code, violation_status, violation_description, inspector_comments
        FROM violations
        WHERE LOWER(TRIM(address)) = %s
    """, (address_clean,))
    violations = cur.fetchall()

    if not violations:
        conn.close()
        return abort(404)

    # Formatting violations list
    violations_list = []
    for v in violations:
        violations_list.append({
            "date": v[0].isoformat(),
            "code": v[1],
            "status": v[2],
            "description": v[3],
            "comments": v[4]
        })

    # Last violation date
    last_violation = max(v[0] for v in violations)

    # Checking scofflaw
    cur.execute("""
        SELECT 1 FROM scofflaws WHERE LOWER(TRIM(address)) = %s LIMIT 1
    """, (address_clean,))
    scofflaw = cur.fetchone() is not None

    conn.close()

    return jsonify({
        "last_violation_date": last_violation.isoformat(),
        "total_violations": len(violations),
        "violations": violations_list,
        "SCOFFLAW": scofflaw
    })

# API endpoint #2: Posts and saves a comment for an address
@app.route('/property/<path:address>/comments/', methods=['POST'])
def add_comment(address):
    data = request.get_json(silent=True) or {}
    author = (data.get('author') or 'anonymous').strip()[:100]
    comment = (data.get('comment') or '').strip()
    if not comment:
        return jsonify({"error": "comment required"}), 400

    dt_str = (data.get('datetime') or '').strip()
    try:
        dt = datetime.fromisoformat(dt_str) if dt_str else datetime.utcnow()
    except Exception:
        dt = datetime.utcnow()

    address_clean = address.strip().lower()

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO comments (address, author, datetime, comment)
        VALUES (%s, %s, %s, %s)
        """,
        (address_clean, author, dt, comment),
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "created"}), 201

# API endpoint #3: displays scofflaws violations on/after 'since'(required)
@app.route('/property/scofflaws/violations/', methods=['GET'])
def scofflaw_violations_since():
    since = request.args.get('since', '').strip()
    if not since:
        return jsonify({"error": "since (YYYY-MM-DD) required"}), 400
    try:
        since_date = datetime.strptime(since, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "since must be YYYY-MM-DD"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT DISTINCT v.address
        FROM violations v
        JOIN scofflaws s
          ON lower(trim(v.address)) = lower(trim(s.address))
        WHERE v.violation_date >= %s
        ORDER BY v.address
        """,
        (since_date,),
    )
    rows = cur.fetchall()
    cur.close(); conn.close()
    return jsonify([r[0] for r in rows]), 200

# Returns JSON errors for API
@app.errorhandler(404)
def not_found(_): return jsonify({"error":"not found"}), 404

@app.errorhandler(400)
def bad_req(e): return jsonify({"error":"bad request","detail":str(e)}), 400

@app.errorhandler(500)
def server_err(_): return jsonify({"error":"internal error"}), 500

if __name__ == '__main__':
    app.run(debug=True)