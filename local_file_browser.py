from flask import Flask, send_from_directory, render_template_string
from threading import Thread
import os
import requests

app = Flask(__name__)
freewrites_dir = os.path.join(os.getcwd(), "TypeWrytes")
server_thread = None

@app.route('/')
def index():
    files = os.listdir(freewrites_dir)
    return render_template_string("""
        <ul>
            {% for file in files %}
            <li><a href="{{ url_for('download_file', filename=file) }}">{{ file }}</a></li>
            {% endfor %}
        </ul>
    """, files=files)

@app.route('/files/<filename>')
def download_file(filename):
    return send_from_directory(freewrites_dir, filename)

def run_server():
    app.run(host='0.0.0.0', port=8080, use_reloader=False)

def start_server():
    global server_thread
    if server_thread is None:
        server_thread = Thread(target=run_server)
        server_thread.start()

def stop_server():
    global server_thread
    if server_thread:
        requests.get('http://localhost:8080/shutdown')
        server_thread.join()
        server_thread = None

@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_func = request.environ.get('werkzeug.server.shutdown')
    if shutdown_func:
        shutdown_func()
    return 'Server shutting down...'