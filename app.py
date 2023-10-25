from flask import Flask, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Configure Google OAuth
google_bp = make_google_blueprint(client_id='YOUR_GOOGLE_CLIENT_ID', client_secret='YOUR_GOOGLE_CLIENT_SECRET', redirect_to='google_login')
app.register_blueprint(google_bp, url_prefix='/google_login')
app.config['GOOGLE_OAUTH_CLIENT_ID'] = 'YOUR_GOOGLE_CLIENT_ID'
app.config['GOOGLE_OAUTH_CLIENT_SECRET'] = 'YOUR_GOOGLE_CLIENT_SECRET'

# Configure Facebook OAuth
facebook_bp = make_facebook_blueprint(client_id='YOUR_FACEBOOK_CLIENT_ID', client_secret='YOUR_FACEBOOK_CLIENT_SECRET', redirect_to='facebook_login')
app.register_blueprint(facebook_bp, url_prefix='/facebook_login')
app.config['FACEBOOK_OAUTH_CLIENT_ID'] = 'YOUR_FACEBOOK_CLIENT_ID'
app.config['FACEBOOK_OAUTH_CLIENT_SECRET'] = 'YOUR_FACEBOOK_CLIENT_SECRET'

@app.route('/')
def home():
    return 'Welcome! <a href="/google">Login with Google</a> | <a href="/facebook">Login with Facebook</a>'

@app.route('/google')
def google_login():
    if not google.authorized:
        return redirect(url_for('google.login'))
    resp = google.get('/plus/v1/people/me')
    assert resp.ok, resp.text
    return 'You are connected with Google as: {0}'.format(resp.json()['displayName'])

@app.route('/facebook')
def facebook_login():
    if not facebook.authorized:
        return redirect(url_for('facebook.login'))
    resp = facebook.get('/me?fields=id,name')
    assert resp.ok, resp.text
    return 'You are connected with Facebook as: {0}'.format(resp.json()['name'])

if __name__=="__main__":
    app.run(host="0.0.0.0")
