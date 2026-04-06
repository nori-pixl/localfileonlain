import os
from flask import Flask, render_template_string, send_from_directory, redirect, url_for, request

app = Flask(__name__)
# ファイルの保存先
UPLOAD_FOLDER = 'shared_files'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

HTML = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>リモートマネージャー</title>
    <style>
        body { font-family: sans-serif; background: #f4f4f9; padding: 20px; display: flex; justify-content: center; }
        .card { background: white; padding: 25px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); width: 100%; max-width: 400px; text-align: center; }
        .icon { font-size: 50px; color: #2196F3; margin-bottom: 10px; }
        input { width: 85%; padding: 12px; margin: 8px 0; border: 1px solid #ddd; border-radius: 5px; font-size: 1.1rem; text-align: center; }
        .btn { background: #2196F3; color: white; border: none; padding: 15px; border-radius: 5px; cursor: pointer; width: 90%; font-size: 1.1rem; font-weight: bold; margin-top: 15px; }
        .file-box { text-align: left; background: #fff; border-radius: 8px; margin-top: 20px; }
        .file-item { display: flex; justify-content: space-between; align-items: center; padding: 15px; border-bottom: 1px solid #eee; }
        .file-info { text-decoration: none; color: #333; font-weight: 500; display: flex; align-items: center; }
        .del-btn { color: #f44336; text-decoration: none; font-size: 0.8rem; border: 1px solid #f44336; padding: 4px 8px; border-radius: 4px; }
        .upload-area { background: #e3f2fd; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="card">
        {% if mode == 'login' %}
            <div class="icon">🌐</div>
            <h2>リモートサービス</h2>
            <p style="color:#666;">表示されている数値を入力</p>
            <input type="text" id="ip" placeholder="IPアドレス (192.168...)">
            <input type="text" id="port" placeholder="ポート番号 (59123)">
            <button class="btn" onclick="location.href='/files'">作成（接続）</button>
        {% else %}
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h3 style="margin:0;">📁 ファイル一覧</h3>
                <a href="/" style="font-size:0.8rem; color:#999; text-decoration:none;">停止</a>
            </div>
            <hr>
            <div class="upload-area">
                <form action="/upload" method="post" enctype="multipart/form-data">
                    <input type="file" name="file" style="width:100%; margin-bottom:10px;">
                    <input type="submit" value="ファイルを追加" class="btn" style="background:#4CAF50; padding:10px; margin:0;">
                </form>
            </div>
            <div class="file-box">
                {% for f in files %}
                <div class="file-item">
                    <a href="/download/{{ f }}" class="file-info">📄 {{ f }}</a>
                    <a href="/delete/{{ f }}" class="del-btn" onclick="return confirm('削除しますか？')">削除</a>
                </div>
                {% endfor %}
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML, mode='login')

@app.route('/files')
def files():
    file_list = sorted([f for f in os.listdir(UPLOAD_FOLDER) if not f.startswith('.')])
    return render_template_string(HTML, mode='files', files=file_list)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if file:
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return redirect(url_for('files'))

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

@app.route('/delete/<filename>')
def delete(filename):
    try:
        os.remove(os.path.join(UPLOAD_FOLDER, filename))
    except:
        pass
    return redirect(url_for('files'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
