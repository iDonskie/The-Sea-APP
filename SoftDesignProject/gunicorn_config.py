# Gunicorn configuration for Render deployment
bind = "0.0.0.0:10000"
workers = 2
worker_class = "sync"
timeout = 120  # Increase timeout to 120 seconds for email sending
keepalive = 5
errorlog = "-"
accesslog = "-"
loglevel = "info"
