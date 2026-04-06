import os
import random
import socket
from flask import Flask, render_template_string, send_from_directory, redirect, url_for, request

app = Flask(__name__)
SHARED_DIR = os.getcwd()

# 共通のデザイン（CSS）
STYLE = """
<style>
    body { font-family: sans-serif; background: #f4f7f6; padding: 20px; display: flex; justify-content: center; }
    .card { background: white; padding: 25px; border-radius: 12px; shadow: 0 4px 10px rgba(0,0,0,0.1); width: 100%; max-width: 400px; text-align: center; }
    input { width: 80%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; }
    .btn { background: #007bff; color: white; border: none; padding: 12px 20px; border-radius: 5px; cursor: pointer; text-decoration: none; display: inline-block; margin-top: 10px; }
    .btn-red { background: #dc3545; padding: 5px 10px; font-size: 0.8rem; }
    .file-item { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #eee; padding: 10px 0; }
    .file-link { text-decoration: none; color: #333; font-weight: bold; flex-grow: 1; text-align: left; }
</style>
"""

# --- ページ1: 接続設定画面 ---
@app.route('/')
def index():
    return render_template_string(f"""
    <!DOCTYPE html>
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1.0">{STYLE}</head>
    <body>
        <div class="card">
            <h2>🔗 接続設定</h2>
            <p>事務所のIPとポートを入力してください</p>
            <input type="text" id="ip" placeholder="例: 192.168.0.10">
            <input type="text" id="port" placeholder="例: 54321">
            <button class="btn" onclick="connect()">作成ボタン（接続）</button>
        </div>
        <script>
            window.onload = () => {{ document.getElementById('ip').value = localStorage.getItem('ip') || ''; }};
            function connect() {{
                const ip = document.getElementById('ip').value;
                const port = document.getElementById('port').value;
                localStorage.setItem('ip', ip);
                location.href = `http://${{ip}}:${{port}}/manager`;
            }}
        </script>
    </body></html>
    """)

# --- ページ2: ファイル管理画面 ---
@app.route('/manager')
def manager():
    files = [f for f in os.listdir(SHARED_DIR) if os.path.isfile(os.path.join(SHARED_DIR, f)) and not f.startswith('.')]
    return render_template_string(f"""
    <!DOCTYPE html>
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1.0">{STYLE}</head>
    <body>
        <div class="card">
            <h3>📁 ファイル一覧</h3>
            {% for file in files %}
            <div class="file-item">
                <a href="/download/{{{{file}}}}" class="file-link">{{{{file}}}}</a>
                <a href="/delete/{{{{file}}}}" class="btn btn-red" onclick="return confirm('削除しますか？')">削除</a>
            </div>
            {% endfor %}
            <br><a href="/" style="font-size: 0.8rem; color: #999;">設定に戻る</a>
        </div>
    </body></html>
    """, files=files)

@app.route('/download/<path:filename>')
def download(filename):
    return send_from_directory(SHARED_DIR, filename, as_attachment=True)

@app.route('/delete/<path:filename>')
def delete(filename):
    try:
        os.remove(os.path.join(SHARED_DIR, filename))
    except: pass
    return redirect(url_for('manager'))

if __name__ == '__main__':
    # ランダムなポートを生成
    random_port = random.randint(49152, 65535)
    
    # 自分のIPを表示（お父さんが同僚に教える用）
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    my_ip = s.getsockname()[0]
    s.close()

    print(f"お父さんのIP: {my_ip}")
    print(f"ランダムポート: {random_port}")
    print(f"URL: http://{my_ip}:{random_port}")

    app.run(host='0.0.0.0', port=random_port)
