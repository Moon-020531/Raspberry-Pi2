from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "<h1>Flask 서버 작동 중!</h1><p>새 SD 카드에서 성공적으로 실행되었습니다.</p>"

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5000)