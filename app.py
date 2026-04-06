import os
from flask import Flask, render_template_string, send_from_directory, redirect, url_for, request

app = Flask(__name__)
# 共有フォルダ（現在のディレクトリ）
SHARED_DIR = os.getcwd()

# 共通のデザイン
STYLE = """
<style>
    body { font-family: -apple-system, sans-serif; background: #f0f2f5; padding: 20px; display: flex; justify-content: center; }
    .card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); width: 100%; max-width: 400px; text-align: center; }
    input { width: 90%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 8px; font-size: 1rem; }
    .btn { background: #007bff; color: white; border: none; padding: 12px 25px; border-radius: 8px; cursor: pointer; text-decoration: none; display: inline-block; width: 90%; font-size: 1rem; }
    .btn-red { background: #ff4d4d; width: auto; padding: 5px 10px; font-size: 0.8rem; margin: 0; }
    .file-item { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #eee; padding: 12px 0; }
    .file-link { text-decoration: none; color: #007bff; font-weight: bold; flex-grow: 1; text-align: left; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; margin-right: 10px; }
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
            <h2>🔗 ファイル共有接続</h2>
            <p>サーバーの情報を確認して接続してください</p>
            <input type="text" id="url" placeholder="URL (例: ://onrender.com)">
            <input type="text" id="port" placeholder="ポート (例: 8080)">
            <button class="btn" onclick="connect()">作成ボタン（接続）</button>
        </div>
        <script>
            window.onload = () => {{ document.getElementById('url').value = location.hostname; }};
            function connect() {{
                const url = document.getElementById('url').value;
                localStorage.setItem('saved_url', url);
                location.href = '/manager';
            }}
        </script>
    </body></html>
    """)

# --- ページ2: ファイル管理画面（表示・ダウンロード・削除） ---
@app.route('/manager')
def manager():
    # 隠しファイル以外のファイルリストを取得
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
                <a href="/delete/{{{{file}}}}" class="btn btn-red" onclick="return confirm('本当に削除しますか？')">削除</a>
            </div>
            {% endfor %}
            <br><a href="/" style="font-size: 0.8rem; color: #999; text-decoration:none;">← 設定に戻る</a>
        </div>
    </body></html>
    """, files=files)

# ダウンロード処理
@app.route('/download/<path:filename>')
def download(filename):
    return send_from_directory(SHARED_DIR, filename, as_attachment=True)

# 削除処理
@app.route('/delete/<path:filename>')
def delete(filename):
    try:
        os.remove(os.path.join(SHARED_DIR, filename))
    except Exception as e:
        print(f"Error deleting file: {{e}}")
    return redirect(url_for('manager'))

if __name__ == '__main__':
    # Renderなどの環境に合わせてポートを自動設定
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
