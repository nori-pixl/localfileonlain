import os
import random
import socket
from flask import Flask, render_template_string, send_from_directory, redirect, url_for

app = Flask(__name__)
SHARED_DIR = os.getcwd()

HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Share</title>
    <style>
        body { font-family: sans-serif; background: #f0f2f5; padding: 20px; display: flex; justify-content: center; }
        .card { background: white; padding: 20px; border-radius: 12px; shadow: 0 4px 10px rgba(0,0,0,0.1); width: 100%; max-width: 400px; text-align: center; }
        input { width: 90%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; }
        .btn { background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; text-decoration: none; display: inline-block; width: 90%; }
        .btn-red { background: #dc3545; width: auto; padding: 5px 10px; font-size: 0.8rem; }
        .item { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #eee; padding: 10px 0; }
        .link { text-decoration: none; color: #007bff; font-weight: bold; flex-grow: 1; text-align: left; }
    </style>
</head>
<body>
    <div class="card">
        {% if mode == 'config' %}
            <h2>Connect</h2>
            <input type="text" id="ip" placeholder="IP">
            <input type="text" id="port" placeholder="Port">
            <button class="btn" onclick="go()">作成</button>
            <script>
                function go() {
                    const ip = document.getElementById('ip').value;
                    const port = document.getElementById('port').value;
                    location.href = '/manager';
                }
            </script>
        {% else %}
            <h3>Files</h3>
            {% for f in files %}
            <div class="item">
                <a href="/download/{{f}}" class="link">{{f}}</a>
                <a href="/delete/{{f}}" class="btn btn-red" onclick="return confirm('OK?')">削除</a>
            </div>
            {% endfor %}
            <br><a href="/">Back</a>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML, mode='config')

@app.route('/manager')
def manager():
    files = [f for f in os.listdir(SHARED_DIR) if os.path.isfile(os.path.join(SHARED_DIR, f)) and not f.startswith('.')]
    return render_template_string(HTML, mode='manager', files=files)

@app.route('/download/<path:filename>')
def download(filename):
    return send_from_directory(SHARED_DIR, filename, as_attachment=True)

@app.route('/delete/<path:filename>')
def delete(filename):
    try:
        os.remove(os.path.join(SHARED_DIR, filename))
    except:
        pass
    return redirect(url_for('manager'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
