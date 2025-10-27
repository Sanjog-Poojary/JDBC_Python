# Drug Store - Python Frontend

This is a minimal Flask frontend for the DRUG_STORE database (SQL schema provided in `DRUG_STORE.sql`). It uses SQLite via SQLAlchemy and seeds the database with sample data derived from the SQL file.

Prerequisites

- Python 3.8+

Quick start (PowerShell)

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python seed.py   # creates sqlite database drugstore.db
python app.py    # starts the Flask dev server

# Open http://127.0.0.1:5000 in your browser
```

What you get

- List and search medicines
- View manufacturers, pharmacies, employees, doctors
- List and add patients
- List and add prescriptions

Notes

- The original SQL was authored for MySQL. This project reproduces the schema using SQLAlchemy models and seeds representative data.
