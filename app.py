import os
import socket
import random
from flask import Flask, render_template_string, send_from_directory, redirect, url_for, request

app = Flask(__name__)
BASE_DIR = os.getcwd()

HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>事務所共有</title>
    <style>
        body { font-family: sans-serif; background: #eef2f3; padding: 20px; display: flex; justify-content: center; }
        .card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); width: 100%; max-width: 450px; text-align: center; }
        input[type="text"] { width: 85%; padding: 12px; margin: 8px 0; border: 1px solid #ddd; border-radius: 8px; font-size: 1rem; }
        .btn { background: #007bff; color: white; border: none; padding: 12px 20px; border-radius: 8px; cursor: pointer; text-decoration: none; display: inline-block; width: 90%; font-size: 1rem; }
        .btn-add { background: #28a745; margin-top: 10px; }
        .btn-del { background: #dc3545; padding: 5px 10px; font-size: 0.8rem; width: auto; }
        .item { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #eee; padding: 12px 0; }
        .link { text-decoration: none; color: #007bff; font-weight: bold; flex-grow: 1; text-align: left; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
        .upload-box { background: #f8f9fa; border: 1px dashed #ccc; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="card">
        {% if mode == 'config' %}
            <h2>🔗 接続設定</h2>
            <p>お父さんのスマホに表示された<br>数値を入力してください</p>
            <input type="text" id="ip" placeholder="IP (例: 192.162.0.100)">
            <input type="text" id="port" placeholder="Port (例: 54321)">
            <button class="btn" onclick="connect()">作成ボタン（接続）</button>
            <script>
                function connect() {
                    const ip = document.getElementById('ip').value;
                    const port = document.getElementById('port').value;
                    if(ip && port) {
                        location.href = `http://${ip}:${port}/manager`;
                    } else {
                        alert('入力してください');
                    }
                }
            </script>
        {% else %}
            <h3>📁 ファイル管理</h3>
            <div class="upload-box">
                <form action="/upload" method="post" enctype="multipart/form-data">
                    <input type="file" name="file" style="margin-bottom:10px;"><br>
                    <input type="submit" value="ファイルを追加" class="btn btn-add">
                </form>
            </div>
            {% for f in files %}
            <div class="item">
                <a href="/download/{{ f }}" class="link">📄 {{ f }}</a>
                <a href="/delete/{{ f }}" class="btn btn-del" onclick="return confirm('本当に削除しますか？')">削除</a>
            </div>
            {% endfor %}
            <br><a href="/" style="color:#999; text-decoration:none; font-size:0.8rem;">← 接続画面へ戻る</a>
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
    files = sorted([f for f in os.listdir(BASE_DIR) if os.path.isfile(os.path.join(BASE_DIR, f)) and not f.startswith('.')])
    return render_template_string(HTML, mode='manager', files=files)

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
    except:
        pass
    return redirect(url_for('manager'))

if __name__ == '__main__':
    # 事務所のWi-Fi内のIPを自動取得
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        my_ip = s.getsockname()[0]
    except:
        my_ip = "127.0.0.1"
    finally:
        s.close()
    
    # 49152〜65535の間でランダムなポートを選択
    my_port = random.randint(49152, 65535)
    
    print(f"--- 起動完了 ---")
    print(f"IP: {my_ip}")
    print(f"Port: {my_port}")
    print(f"同僚に教えてください: http://{my_ip}:{my_port}")
    
    app.run(host='0.0.0.0', port=my_port)
