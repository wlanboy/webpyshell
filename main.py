import os
import secrets
from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit
from werkzeug.security import generate_password_hash, check_password_hash
import pty
import subprocess

app = Flask(__name__)
# Generate a random SECRET_KEY for each run
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
socketio = SocketIO(app)

# Session management for terminals
terminals = {}

# Random password for login
root_password = secrets.token_urlsafe(16)
root_password_hash = generate_password_hash(root_password)

print(f"root password for login is: {root_password}")
print(f"SECRET_KEY for this session is: {app.config['SECRET_KEY']}")

@app.route('/')
def index():
    if 'logged_in' not in session or not session.get('password_hash') or not check_password_hash(session.get('password_hash'), root_password):
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if check_password_hash(root_password_hash, password):
            session['logged_in'] = True
            session['password_hash'] = root_password_hash
            return redirect(url_for('index'))
        else:
            return 'Invalid password', 401
    return render_template('login.html')

@socketio.on('connect')
def handle_connect():
    if 'logged_in' not in session or not session.get('password_hash') or not check_password_hash(session.get('password_hash'), root_password):
        return False  # Reject connection

@socketio.on('create_terminal')
def create_terminal_session():
    pid, fd = pty.fork()
    if pid == 0:
        subprocess.run(['bash'])
        os._exit(0)
    else:
        terminals[request.sid] = fd
        emit('terminal_created')

@socketio.on('terminal_input')
def handle_terminal_input(data):
    if request.sid in terminals:
        os.write(terminals[request.sid], data['input'].encode())

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in terminals:
        os.close(terminals[request.sid])
        del terminals[request.sid]

def read_output():
    while True:
        socketio.sleep(0.01)
        for sid, fd in list(terminals.items()):
            try:
                output = os.read(fd, 4096).decode()
                if output:
                    socketio.emit('terminal_output', {'output': output}, room=sid)
            except OSError:
                if sid in terminals:
                    del terminals[sid]

if __name__ == '__main__':
    socketio.start_background_task(target=read_output)
    socketio.run(app, port=2100, host="0.0.0.0", debug=True)