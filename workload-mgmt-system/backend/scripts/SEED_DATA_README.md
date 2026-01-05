# Seed Data Instructions

This document explains how to populate the database with test data for the WAM system.

## Option 1: Using Python Script (Recommended)

The Python script automatically generates usernames and properly hashes passwords.

### Steps:

1. **Make sure the database is set up:**
   ```bash
   # Ensure tables are created
   # Run migrations if needed
   ```

2. **Run the staff columns migration first (REQUIRED):**
   ```bash
   cd backend
   python scripts/add_staff_columns.py
   ```
   This adds: designation, specialization, experience_years, username columns

3. **Run the username migration (if not done):**
   ```bash
   cd backend
   python scripts/add_username_column.py
   ```
   This generates usernames for existing staff

4. **Run the seed data script:**
   ```bash
   cd backend
   python scripts/seed_data.py
   ```

4. **Verify the data:**
   - Check that staff members were created with usernames
   - Verify domains, programs, and task templates exist

## Option 2: Using SQL Script

If you prefer SQL, you can use the SQL script, but note that password hashes need to be generated properly.

### Steps:

1. **Run the staff columns migration first (REQUIRED):**
   ```bash
   cd backend
   python scripts/add_staff_columns.py
   ```

2. **Run the username migration:**
   ```bash
   cd backend
   python scripts/add_username_column.py
   ```

3. **Execute the SQL script:**
   ```bash
   # Using MySQL command line
   mysql -u root -p wam_db < backend/scripts/seed_data.sql
   
   # Or using MySQL Workbench
   # Open and execute backend/scripts/seed_data.sql
   ```

   **Note:** The SQL script has placeholder password hashes. You'll need to update them with proper bcrypt hashes, or use the Python script instead.

## Option 3: Using Frontend (Manual Entry)

You can also create data manually through the frontend:

### Steps:

1. **Login as Admin:**
   - Username: `adm1`
   - Password: `adm1`

2. **Create Staff Members:**
   - Go to "Staff Management"
   - Click "Add Staff"
   - Fill in the form (username will be auto-generated)
   - Password will default to username

3. **Create Domains:**
   - Go to "Course Management" or use API
   - Create domains (Computing, Engineering, etc.)

4. **Create Programs:**
   - Create programs under domains

5. **Create Task Templates:**
   - Go to "Task Management" → "Task Templates"
   - Create templates for lectures, labs, exams, etc.

6. **Create Task Instances:**
   - Go to "Task Management" → "Task Instances"
   - Create instances for specific semesters

## Test Credentials

After seeding, you can use these credentials:

### Academic Staff:
- `sf1` / `sf1` - Dr. John Smith (Professor)
- `sf2` / `sf2` - Dr. Sarah Johnson (Associate Professor)
- `sf3` / `sf3` - Dr. Michael Williams (Senior Lecturer I)
- `sf4` / `sf4` - Dr. Emily Brown (Lecturer)
- `sf5` / `sf5` - Dr. David Davis (Senior Lecturer II)
- `sf6` / `sf6` - Dr. Lisa Anderson (Lecturer)
- `sf7` / `sf7` - Dr. Robert Taylor (Professor - Mathematics)
- `sf8` / `sf8` - Dr. Maria Garcia (Associate Professor - Physics)

### Admin:
- `adm1` / `adm1` - Admin User

### Management:
- `adm2` / `adm2` - Management User

## What Gets Created

The seed script creates:

1. **10 Designation Workload Policies** - For different staff designations
2. **10 Staff Members** - Mix of academic, admin, and management
3. **4 Domains** - Computing, Engineering, Business, Science
4. **6 Programs** - BSCS, BSSE, MSCS, BSIT, BE, BBA
5. **8 Program Sections** - Sections A, B, C for various programs
6. **12 Task Templates** - Lectures, labs, exams, admin, research tasks
7. **16 Task Instances** - Approved and draft tasks for semester 2025S1
8. **10 Assignments** - Sample staff-to-task assignments
9. **3 Staff Availability Records** - Leave and unavailability records

## Troubleshooting

### If staff usernames are not generated:
- Make sure you ran `add_username_column.py` first
- Check that the `username` column exists in the `staff` table

### If passwords don't work:
- The Python script properly hashes passwords
- If using SQL, you need to generate bcrypt hashes manually
- Default password is the same as username

### If foreign key errors occur:
- Make sure to run seed scripts in order:
  1. Designation policies
  2. Staff
  3. Domains
  4. Programs
  5. Program sections
  6. Task templates
  7. Task instances
  8. Assignments
  9. Staff availability

## Resetting Seed Data

To reset and re-seed:

```sql
-- WARNING: This will delete all data!
TRUNCATE TABLE assignments;
TRUNCATE TABLE staff_availability;
TRUNCATE TABLE task_instances;
TRUNCATE TABLE task_templates;
TRUNCATE TABLE program_sections;
TRUNCATE TABLE programs;
TRUNCATE TABLE domains;
TRUNCATE TABLE staff;
TRUNCATE TABLE designation_workload_policies;
```

Then run the seed script again.

