from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/services')
def services():
    return render_template('services.html')

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
