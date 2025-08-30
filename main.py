from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

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