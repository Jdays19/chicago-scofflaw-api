# API Documentation

Base URL: http://127.0.0.1:5000

### **GET /**  
Checks if the API is running.

**Response 200 (text/plain)**  
- 'API is currently running.'

---

## 1. Get Property Details

### **GET /property/{address}/**  
Purpose: Retrieves violation details for a given property.  
- `address`: string

**Response 200 (application/json)**  
```json
{
  "last_violation_date": "YYYY-MM-DD",
  "total_violations": 3,
  "violations": [
    {
      "date": "2025-01-01",
      "code": "HV01",
      "status": "Open",
      "description": "High weeds on property",
      "comments": "Initial notice sent"
    }
  ],
  "SCOFFLAW": true
}
```

**Response 400 (application/json)**
```json
{ "error": "not found" }
```
--- 

## 2. Add Comment to Property
### **POST /property/{address}/comments/**
Purpose: Adds a comment for a property.
- `address`: string

**Request JSON**
```json
{
  "author": "John Doe",
  "comment": "Needs reinspection.",
  "datetime": "2025-08-20T12:30:00"
}
```
**Response 201 (application/json)**
```json
{ "status": "created" }
```

**Response 400**
```json
{ "error": "bad request", "detail": "Invalid JSON format" }
```
--- 

## 3. Get Scofflaw Addresses Since Date
### **GET /property/scofflaws/violations/**
Purpose: Retrieves scofflaw addresses with violations since a given date.

#### **Query Parameters:**
`since (required): string, format YYYY-MM-DD`

**Response 200 (application/json)**
```json
[
  "123 Main St",
  "456 Oak Ave"
]
```
**Response 400**
```json
{ "error": "since (YYYY-MM-DD) required" }
```
