# Data Directory

This directory contains the application's database files.

## Files

- `marketplace.db` - Main application database
- `database.db` - Secondary/backup database (if exists)

## ⚠️ Important Notes

- **Backup these files regularly** - they contain all your application data
- **Do not manually edit** database files - use the scripts in `scripts/database/` instead  
- **Keep this directory secure** - contains sensitive user data
- **Version control**: Consider adding `*.db` to `.gitignore` for privacy

## Database Management

For database maintenance, use the scripts in:
- `scripts/database/` - Database maintenance
- `scripts/admin/` - Admin-related database operations
- `scripts/testing/` - Test data management