from flask import Flask, render_template, request, redirect, url_for, session
import subprocess
import logging
import secrets

app = Flask(__name__)

# Use gunicorn's logger if running under gunicorn
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
else:
    logging.basicConfig(level=logging.INFO)

app.secret_key = secrets.token_urlsafe(16)
ACCESS_KEY = secrets.token_urlsafe(16)
app.logger.info(f"Access Key: {ACCESS_KEY}")

def is_authenticated():
    """Prüft, ob der Benutzer den korrekten Schlüssel in der Session hat."""
    return session.get('key_ok') == ACCESS_KEY

@app.before_request
def check_access():
    """Wird vor jeder Anfrage ausgeführt, um den Benutzer zu authentifizieren."""
    if request.endpoint not in ['login', 'static'] and not is_authenticated():
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_key = request.form.get('key')
        if user_key == ACCESS_KEY:
            session['key_ok'] = ACCESS_KEY
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Ungültiger Schlüssel.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('key_ok', None)
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def index():
    output = None
    command = ''
    if request.method == 'POST':
        command = request.form.get('command')
        if command:
            try:
                result = subprocess.run(
                    command,
                    shell=True,
                    check=True,
                    capture_output=True,
                    text=True,
                    encoding='utf-8'
                )
                output = result.stdout + result.stderr
            except subprocess.CalledProcessError as e:
                output = f"Fehler bei der Ausführung:\n{e.stdout}\n{e.stderr}"
            except Exception as e:
                output = f"Ein Fehler ist aufgetreten: {str(e)}"

    return render_template('index.html', output=output, command=command)

if __name__ == '__main__':
    app.run(debug=True)