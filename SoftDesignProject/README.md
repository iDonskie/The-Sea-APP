# Student Emporium - Marketplace Platform

A modern Flask-based marketplace application for students to buy and sell items with integrated chat functionality.

## 🚀 Quick Start

1. **Run the application:**
   ```bash
   python app.py
   ```

2. **Create admin account:**
   ```bash
   python scripts/admin/quick_admin_setup.py
   ```

## 📁 Project Structure

```
SoftDesignProject/
├── app.py                 # Main Flask application
├── data/                  # Database files
├── database/             # Database utilities
├── scripts/              # Utility scripts
│   ├── admin/           # Admin management
│   ├── database/        # Database maintenance
│   └── testing/         # Test scripts
├── static/              # Static assets (CSS, JS, images)
├── templates/           # HTML templates
└── SECURITY.md         # Security documentation
```

## 🔧 Features

- **Marketplace**: Buy and sell items with categories
- **Chat System**: Real-time messaging between users
- **Admin Panel**: Moderate listings and manage users
- **Image Support**: Upload and view product images
- **User Authentication**: Secure login and registration

## 🛠️ Administration

- Access admin panel at `/admin` after creating admin account
- Use scripts in `scripts/admin/` for admin management
- Database maintenance scripts in `scripts/database/`

## 📝 Development

- Test scripts available in `scripts/testing/`
- Database files stored in `data/`
- Follow security guidelines in `SECURITY.md`