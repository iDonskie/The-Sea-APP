# Database Scripts

This directory contains scripts for database maintenance and management.

## Scripts

- `fix_database.py` - General database repair
- `fix_correct_database.py` - Correct database structure issues  
- `fix_db_columns.py` - Fix column-related issues
- `check_db_status.py` - Check database health and status
- `update_messages_table.py` - Update message table structure

## Usage

⚠️ **Warning**: Always backup your database before running maintenance scripts!

Run scripts from the project root directory:
```bash
python scripts/database/script_name.py
```

Database files are stored in the `data/` directory.