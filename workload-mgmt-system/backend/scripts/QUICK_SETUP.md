# Quick Database Setup Guide

## One-Command Setup

```bash
cd backend
python scripts/setup_complete_database.py
```

That's it! The script will:
- ✅ Create all 14 tables
- ✅ Add missing columns
- ✅ Create indexes
- ✅ Set up foreign keys
- ✅ Handle errors gracefully

## What Gets Created

### All Tables:
1. `domains` - Academic domains
2. `programs` - Degree programs  
3. `program_sections` - Program sections
4. `staff` - Staff members (with all fields)
5. `designation_workload_policies` - Workload limits
6. `task_templates` - Reusable task definitions
7. `task_instances` - Specific task executions
8. `assignments` - Staff-to-task assignments
9. `staff_availability` - Leave records
10. `change_requests` - Change requests
11. `modules` - Course modules
12. `module_sections` - Module sections
13. `tariffs` - Tariff rules
14. `tasks` - Legacy tasks (backward compatibility)

### All Columns:
- Staff table: username, designation, qualification, specialization, department, role, experience_years, skills, password_hash, is_active, etc.
- Assignments table: task_instance_id (new), task_id (legacy, nullable)
- All other tables with complete schema

### All Indexes:
- Unique index on `staff.username`
- Indexes on frequently queried columns
- Foreign key indexes

## After Setup

1. **Seed Data:**
   ```bash
   python scripts/seed_data.py
   ```

2. **Start Backend:**
   ```bash
   python -m uvicorn app.main:app --reload
   ```

3. **Verify:**
   - Open: `http://localhost:8000/docs`
   - Check dashboard: Should show real counts from database

## Troubleshooting

**Error: "Table already exists"**
- ✅ Normal - script skips existing tables

**Error: "Column already exists"**  
- ✅ Normal - script skips existing columns

**Error: "Access denied"**
- Check database credentials
- Grant permissions: `GRANT ALL ON wam_db.* TO 'root'@'localhost';`

**Error: "Module not found"**
- Install dependencies: `pip install -r requirements.txt`
- Make sure you're in `backend/` directory

## Alternative: SQL Script

If you prefer SQL:

```bash
mysql -u root -p wam_db < backend/scripts/setup_database.sql
```

**Note:** Python script is recommended as it handles edge cases better.

## Verification

Check tables exist:
```sql
USE wam_db;
SHOW TABLES;
```

Should show 14 tables.

Check staff table structure:
```sql
DESCRIBE staff;
```

Should show all columns including username, department, role, etc.

## Safe to Run Multiple Times

The script is **idempotent** - safe to run multiple times. It will:
- Skip existing tables/columns
- Only add what's missing
- Never delete data

