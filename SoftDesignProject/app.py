from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/services')
def services():
    services = [
        {
            "name": "Modern Mist",
            "short_desc": "Affordable handmade perfumes by students.",
            "description": "ScentScape offers long-lasting, student-made fragrances crafted with love and creativity. Visit us to explore signature scents inspired by campus life.",
            "image": ['services/perfume1.jpg', "services/perfume2.jpg"]
        },
        {
            "name": "Cookies by Clark",
            "short_desc": "Freshly baked cookies made daily.",
            "description": "Soft, chewy, and irresistible — our cookies are baked fresh every day by student bakers. Perfect for snacks or gifts!",
            "image": ["services/cookie1.jpeg", "services/cookie2.jpeg"]
        },
        {
            "name": "Petal Express",
            "short_desc": "Fresh flowers on the go.",
            "description": "Petal Express offers affordable blooms, dedicated to making you smile—straight from the heart. 💐",
            "image": ["services/flower1.jpg", "services/flower2.jpg"]
        },
        {
            "name": "Hiro Bites",
            "short_desc": "Creamy graham bars made by students.",
            "description": "Unang kagat, Mmhmm ang sarap! Hiro Bites is ready to sweeten your day ✨",
            "image": ["services/graham.jpg", "services/graham2.jpg"]
        }
    ]
    return render_template('services.html', services=services)

@app.route('/marketplace')
def marketplace():
    items = [
        {'name': 'Calculator', 'price': '900', "image": "item1.jpeg", "description": "A high-quality calculator for all your mathematical needs."},
        {'name': 'Headphones', 'price': '1200', "image": "item2.jpeg", "description": "Experience immersive sound with these comfortable headphones."},
        {'name': 'Lamp', 'price': '500', "image": "item3.jpeg", "description": "A stylish lamp to brighten up your workspace or living area."},
        {'name': 'Switch', 'price': '9900', "image": "item4.jpeg", "description": "A versatile switch for your gaming and entertainment needs."}, 
    ]
    return render_template('marketplace.html', items=items)

@app.route('/organizations')
def organizations():
    return render_template('organizations.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        org = request.form['org']
        return f"Thanks for registering, {name}! We sent a confirmation to {email}."
    
    return render_template('register.html')

if __name__ == "__main__":
    app.run(debug=True)
