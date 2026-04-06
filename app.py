import os
import socket
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)

# 共有するファイルの場所（現在のフォルダ）
SHARED_DIR = os.getcwd()

# 1. メイン画面（ファイル一覧を表示）
@app.route('/')
def index():
    # フォルダ内のファイルリストを取得（pyファイルなどは除外すると安全）
    files = [f for f in os.listdir(SHARED_DIR) if os.path.isfile(os.path.join(SHARED_DIR, f))]
    
    # 実行中のサーバーのIPアドレスを取得（表示用）
    try:
        hostname = socket.gethostname()
        current_ip = socket.gethostbyname(hostname)
    except:
        current_ip = "localhost"

    return render_template('index.html', files=files, ip=current_ip)

# 2. ファイルダウンロード用
@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(SHARED_DIR, filename, as_attachment=True)

# 実行設定
if __name__ == '__main__':
    # Renderなどのクラウド環境では環境変数 PORT が割り振られます
    # ローカルで動かす場合は 5000 番をデフォルトにします
    port = int(os.environ.get("PORT", 5000))
    
    print(f"--- サーバーを起動します ---")
    print(f"アクセスURL例: http://localhost:{port}")
    
    # host='0.0.0.0' にすることで、同じWi-Fi内の他のスマホからも接続可能になります
    app.run(host='0.0.0.0', port=port)
