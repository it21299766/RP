# Backend Startup Guide

This guide explains how to start the WAM backend server.

## Prerequisites

1. **Python 3.8+** installed
2. **MySQL** installed and running
3. **Database `wam_db`** created
4. **Environment variables** configured in `.env` file

## Quick Start

### Step 1: Create .env File

Copy `.env.example` to `.env` and update with your database credentials:

```bash
copy .env.example .env
```

Edit `.env` file and update:
- `DATABASE_URL`: MySQL connection string
- `JWT_SECRET_KEY`: Secret key for JWT tokens (change in production)

Example `.env` file:
```
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3307/wam_db
JWT_SECRET_KEY=your-secret-key-here-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_SECONDS=86400
```

### Step 2: Install Dependencies (First Time Only)

```bash
pip install -r requirements.txt
```

### Step 3: Run Startup Script

Simply double-click `start_backend.bat` or run from command line:

```bash
start_backend.bat
```

The script will:
1. ✅ Check if `.env` file exists
2. ✅ Verify Python is installed
3. ✅ Check dependencies
4. ✅ Run database migrations (001-006)
5. ✅ Start the FastAPI server

## Manual Start (Alternative)

If you prefer to start manually:

### Run Migrations First

```bash
cd db-migrations
mysql -u root -p wam_db < 001_add_staff_base_columns.sql
mysql -u root -p wam_db < 002_add_auth_columns.sql
mysql -u root -p wam_db < 003_add_username_index.sql
mysql -u root -p wam_db < 004_add_task_instance_id.sql
mysql -u root -p wam_db < 005_add_profile_picture_column.sql
mysql -u root -p wam_db < 006_add_created_at_to_change_requests.sql
cd ..
```

### Start Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Access Points

- **API Server**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## Troubleshooting

### Error: .env file not found
- Create `.env` file in `backend/` directory
- Copy from `.env.example` and update credentials

### Error: DATABASE_URL not set
- Make sure `.env` file exists and contains `DATABASE_URL`
- Check file is in `backend/` directory (not in parent folder)

### Error: MySQL connection failed
- Verify MySQL is running
- Check database `wam_db` exists: `CREATE DATABASE wam_db;`
- Verify credentials in `.env` file
- Check MySQL port (default: 3306, or 3307 in example)

### Error: Migration failed
- Ensure MySQL is running
- Check database exists
- Verify MySQL root password is correct
- Check migration files are in `db-migrations/` directory

### Error: Module not found
- Install dependencies: `pip install -r requirements.txt`
- Use virtual environment (recommended): `python -m venv venv` then `venv\Scripts\activate`

## Virtual Environment (Recommended)

For production or to avoid package conflicts:

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run startup script
start_backend.bat
```

