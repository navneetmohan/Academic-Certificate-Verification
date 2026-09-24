# Backend Layer: FastAPI Academic Credential Engine

FastAPI backend application orchestrating certificate issuance, deterministic ReportLab PDF generation with QR codes, cryptographic SHA-256 calculation, and Ethereum Web3 interaction.

## Architecture

- **Framework**: FastAPI (Python 3.10+)
- **ORM / Database**: SQLAlchemy (SQLite out-of-the-box or PostgreSQL via `DATABASE_URL`)
- **Blockchain Client**: Web3.py connecting to Hardhat localnet (`http://127.0.0.1:8545`)
- **PDF Generation**: ReportLab with embedded QR codes pointing to `/verify/{id}`
- **Authentication**: JWT with native bcrypt password hashing

## Commands

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# 3. Install requirements
pip install -r requirements.txt

# 4. Run automated tests
python -m pytest -v

# 5. Start API server
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
