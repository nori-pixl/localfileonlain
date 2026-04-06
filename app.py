from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__)
SHARED_DIR = os.getcwd()

# 1. 最初のアドレス設定画面
@app.route('/')
def index():
    return render_template('index.html')

# 2. ファイル共有実行画面
@app.route('/share')
def share():
    ip = request.args.get('ip')
    port = request.args.get('port')
    files = os.listdir(SHARED_DIR)
    # 実際にはこのアプリ自体がそのIP/Portで動いている必要があります
    return render_template('share.html', ip=ip, port=port, files=files)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(SHARED_DIR, filename)

if __name__ == '__main__':
    # どのアドレスからでもアクセスを許可
    app.run(host='0.0.0.0', port=5000) 
