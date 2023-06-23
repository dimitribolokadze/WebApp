from flask import Flask, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
import requests
import os
import secrets

def generate_secret_key():
    return secrets.token_hex(16)

secret_key = generate_secret_key()

app = Flask(__name__)
app.secret_key = secret_key

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/weather', methods=['GET', 'POST'])
def weather():
    if request.method == 'POST':
        location = request.form['location']
        api_key = 'cccb7e39abfbe6a058cb1ca4edc0ca3e'
        base_url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric'

        response = requests.get(base_url)
        weather_data = response.json()

        if response.status_code == 200:
            temperature = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
            description = weather_data['weather'][0]['description']

            return render_template('weather.html', temperature=temperature, humidity=humidity, description=description)
        else:
            flash('Invalid location. Please try again.', 'error')
            return redirect('/weather')

    return render_template('search.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
