from flask import Flask, render_template, request, redirect, url_for, session, Response
import subprocess
import logging
import secrets

app = Flask(__name__)

SAFE_BUSYBOX_COMMANDS = {
    "ls", "cat", "echo", "head", "tail", "grep", "fgrep", "egrep",
    "awk", "sed", "cut", "sort", "uniq", "wc", "xxd", "base64",
    "date", "cal", "pwd", "printf", "true", "false", "sleep",
    "time", "uptime", "whoami", "which", "test", "expr",
    "dirname", "basename", "rev", "fold", "strings", "stat",
    "arping",
    "nc",
    "nslookup",
    "ping",
    "wget",
    "curl",
    "traceroute",
    "traceroute6",
    "ssl_client",
    "hostname",
    "dnsdomainname"
}


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

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/stream')
def stream():
    command = request.args.get('command', '').strip()

    # 1. Hilfe anzeigen
    if command == "?":
        def helpgen():
            yield "data: Verfügbare Befehle:\n\n"
            for cmd in sorted(SAFE_BUSYBOX_COMMANDS):
                yield f"data:   {cmd}\n\n"
            yield "data: [END]\n\n"
        return Response(helpgen(), mimetype='text/event-stream')

    # 2. Leere Eingaben blockieren
    if not command:
        def deny():
            yield "data: ERROR: Kein Befehl.\n\n"
            yield "data: [END]\n\n"
        return Response(deny(), mimetype='text/event-stream')

    # 3. sudo blockieren
    if "sudo" in command.split():
        def deny():
            yield "data: ERROR: sudo ist nicht erlaubt.\n\n"
            yield "data: [END]\n\n"
        return Response(deny(), mimetype='text/event-stream')

    # 4. Whitelist prüfen
    cmd_name = command.split()[0]
    if cmd_name not in SAFE_BUSYBOX_COMMANDS:
        def deny():
            yield f"data: ERROR: '{cmd_name}' ist nicht erlaubt.\n\n"
            yield "data: [END]\n\n"
        return Response(deny(), mimetype='text/event-stream')

    # 5. BusyBox ausführen
    def generate():
        try:
            process = subprocess.Popen(
                ["busybox", "sh", "-c", command],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            for line in process.stdout:
                yield f"data: {line.rstrip()}\n\n"

            process.wait()

        except Exception as e:
            yield f"data: ERROR: {str(e)}\n\n"

        yield "data: [END]\n\n"

    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)