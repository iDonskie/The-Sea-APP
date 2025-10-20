# Admin Scripts

This directory contains scripts for managing administrators and admin-related tasks.

## Scripts

### Admin Management
- `quick_admin_setup.py` - Quick setup for creating admin accounts
- `create_admin.py` - Create new admin users
- `check_admin.py` - Verify admin account status
- `make_admin.py` - Promote users to admin
- `fix_admin_password.py` - Reset admin passwords
- `approve_pending.py` - Approve pending marketplace listings

### User Management
- `manage_users.py` - **MAIN TOOL** - Interactive user management system
- `check_users.py` - List all users in database
- `reset_all_passwords.py` - Reset all passwords to "123" for easy login

## Usage

Run any script from the project root directory:
```bash
python scripts/admin/script_name.py
```