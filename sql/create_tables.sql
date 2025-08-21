CREATE TABLE violations (
    id SERIAL PRIMARY KEY,
    address TEXT,
    violation_date DATE,
    violation_code TEXT,
    violation_status TEXT,
    violation_description TEXT,
    inspector_comments TEXT
);

CREATE TABLE scofflaws (
    id SERIAL PRIMARY KEY,
    address TEXT,
    court_case_number TEXT,
    owner_list_date DATE
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    address TEXT,
    author TEXT,
    datetime TIMESTAMP,
    comment TEXT
);
