# SEA - Student's Emporium for All

A marketplace platform for students to buy and sell items, with built-in messaging functionality.

## Features
- 🛒 Buy and sell marketplace
- 💬 Real-time messaging between users
- 📸 Image uploads for listings and messages
- 👤 User authentication and profiles
- 🛡️ Admin dashboard for moderation

## Local Development

### Prerequisites
- Python 3.8+
- pip

### Setup
1. Clone the repository
```bash
git clone https://github.com/fishbones-09/softdestypeshit.git
cd softdestypeshit/SoftDesignProject
```

2. Create virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Initialize database
```bash
python database/init_db.py
python database/add_edited_at_column.py
```

5. Run the application
```bash
python run.py
```

Visit `http://localhost:5000` in your browser.

## Deployment

### Environment Variables
Set these environment variables for production:
- `SECRET_KEY` - A strong random secret key
- `FLASK_ENV=production` - Enables production settings

### Deploy to Render (Recommended)
1. Push code to GitHub
2. Go to [render.com](https://render.com) and sign up
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Build Command**: `pip install -r requirements.txt && python database/init_db.py && python database/add_edited_at_column.py`
   - **Start Command**: `gunicorn app:app`
   - **Environment Variables**: Add `SECRET_KEY` with a random value
6. Click "Create Web Service"

### Deploy to PythonAnywhere
1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload files or clone from GitHub
3. Set up virtual environment and install requirements
4. Configure web app in dashboard
5. Set working directory and WSGI file
6. Reload web app

## License
MIT License
