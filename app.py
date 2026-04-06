import os
from flask import Flask, render_template_string, send_from_directory

app = Flask(__name__)
# サーバー上の現在のディレクトリ
SHARED_DIR = os.getcwd()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ファイル共有</title>
</head>
<body>
    <h1>📁 ファイル共有サイト</h1>
    <ul>
        {% for file in files %}
        <li><a href="/download/{{ file }}">{{ file }}</a></li>
        {% endfor %}
    </ul>
</body>
</html>
"""

@app.route('/')
def index():
    files = [f for f in os.listdir(SHARED_DIR) if os.path.isfile(os.path.join(SHARED_DIR, f)) and not f.startswith('.')]
    return render_template_string(HTML_TEMPLATE, files=files)

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(SHARED_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
