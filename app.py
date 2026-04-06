import random
import socket
from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

# 共有したいファイルが置かれているディレクトリ（現在のフォルダ）
SHARED_DIR = os.getcwd()

@app.route('/')
def index():
    # フォルダ内のファイル一覧を取得
    files = os.listdir(SHARED_DIR)
    return render_template('index.html', files=files)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(SHARED_DIR, filename)

def get_random_port():
    """使用されていないランダムなポートを返す"""
    while True:
        port = random.randint(49152, 65535)
        # ポートが使用中かチェック
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                return port

if __name__ == '__main__':
    # 指定のIP（192.162.0.1など）に書き換えてください。
    # 0.0.0.0にするとネットワーク内の他端末からもアクセス可能です。
    my_ip = '192.162.0.100' 
    random_port = get_random_port()
    
    print(f"--- 共有サイトを起動します ---")
    print(f"URL: http://{my_ip}:{random_port}")
    
    # 実行（デバッグモードはオフ）
    app.run(host='0.0.0.0', port=random_port)
