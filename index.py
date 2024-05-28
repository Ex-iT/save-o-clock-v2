from flask import Flask, render_template
from flask_minify import minify
from datetime import datetime
from pytz import timezone
import secrets

NONCE = ''
TIMEZONE = 'Europe/Amsterdam'

app = Flask(__name__)
minify(app=app, html=True, js=True, cssless=True)

def set_nonce():
    global NONCE
    NONCE = secrets.token_urlsafe()

def get_current_time():
    global TIMEZONE
    utc = timezone('UTC')
    now = utc.localize(datetime.utcnow())
    amsterdam = timezone(TIMEZONE)

    return now.astimezone(amsterdam).strftime('%H:%M')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path):
    set_nonce()
    
    return render_template('index.html', timezone=TIMEZONE, current_time=get_current_time(), nonce=NONCE)

@app.after_request
def after_request(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'no-referrer-when-downgrade'
    response.headers['Permissions-Policy'] = 'geolocation=(self), microphone=()'
    response.headers['Content-Security-Policy'] = f'default-src \'self\'; base-uri \'none\'; object-src \'none\'; style-src \'self\' \'unsafe-inline\' fonts.googleapis.com; font-src \'self\' fonts.gstatic.com; script-src \'self\' \'nonce-{NONCE}\' \'strict-dynamic\''

    return response