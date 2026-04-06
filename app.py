import os
from flask import Flask, render_template_string, send_from_directory, redirect, url_for, request

app = Flask(__name__)
# フォルダのパス設定
BASE_DIR = os.getcwd()

HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Manager</title>
    <style>
        body { font-family: sans-serif; background: #f0f2f5; padding: 20px; display: flex; justify-content: center; }
        .card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); width: 100%; max-width: 500px; text-align: center; }
        .upload-section { background: #e9ecef; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
        input[type="file"] { margin: 10px 0; }
        .btn { background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; text-decoration: none; display: inline-block; }
        .btn-red { background: #dc3545; padding: 5px 10px; font-size: 0.8rem; margin-left: 10px; }
        .item { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #eee; padding: 12px 0; }
        .link { text-decoration: none; color: #007bff; font-weight: bold; flex-grow: 1; text-align: left; }
        .folder { color: #f39c12; margin-right: 5px; }
    </style>
</head>
<body>
    <div class="card">
        {% if mode == 'config' %}
            <h2>Connect</h2>
            <button class="btn" onclick="location.href='/manager'">作成（接続）</button>
        {% else %}
            <h3>📁 ファイル管理</h3>
            <div class="upload-section">
                <form action="/upload" method="post" enctype="multipart/form-data">
                    <input type="file" name="file">
                    <input type="submit" value="アップロード" class="btn">
                </form>
            </div>
            <div style="text-align: left; margin-bottom: 10px;">
                <a href="/manager?path={{ parent_path }}">⬅ 戻る</a>
            </div>
            {% for d in dirs %}
            <div class="item">
                <a href="/manager?path={{ current_path }}/{{ d }}" class="link"><span class="folder">📁</span> {{ d }}</a>
            </div>
            {% endfor %}
            {% for f in files %}
            <div class="item">
                <a href="/download/{{ current_path }}/{{ f }}" class="link">📄 {{ f }}</a>
                <a href="/delete/{{ current_path }}/{{ f }}" class="btn btn-red" onclick="return confirm('削除？')">削除</a>
            </div>
            {% endfor %}
            <br><a href="/">Top</a>
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
    rel_path = request.args.get('path', '').strip('/')
    abs_path = os.path.join(BASE_DIR, rel_path)
    
    if not os.path.exists(abs_path) or not abs_path.startswith(BASE_DIR):
        return redirect(url_for('manager'))

    items = os.listdir(abs_path)
    dirs = [i for i in items if os.path.isdir(os.path.join(abs_path, i)) and not i.startswith('.')]
    files = [i for i in items if os.path.isfile(os.path.join(abs_path, i)) and not i.startswith('.')]
    
    parent_path = os.path.dirname(rel_path)
    return render_template_string(HTML, mode='manager', dirs=dirs, files=files, current_path=rel_path, parent_path=parent_path)

@app.route('/upload', method=['POST']) # method修正
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if file:
        file.save(os.path.join(BASE_DIR, file.filename))
    return redirect(url_for('manager'))

@app.route('/download/<path:filename>')
def download(filename):
    return send_from_directory(BASE_DIR, filename, as_attachment=True)

@app.route('/delete/<path:filename>')
def delete(filename):
    try:
        os.remove(os.path.join(BASE_DIR, filename))
    except: pass
    return redirect(url_for('manager'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
