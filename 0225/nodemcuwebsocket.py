from gevent import monkey
monkey.patch_all()
from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__, template_folder='.')
socketio = SocketIO(app, 
                    async_mode='gevent', 
                    engineio_logger=True, 
                    cors_allowed_origins="*")

@socketio.on('join_web')
def join_web(message):
    print("🌐 [WEB] 웹 브라우저가 'WEB' 방에 접속했습니다!")
    join_room('WEB')
    
@socketio.on('join_dev')
def join_dev(message):
    print("🤖 [ESP32] 기기가 'DEV' 방에 접속했습니다!")
    join_room('DEV')

@socketio.on('led')        
def handle_led(message):
    print(f"💡 [WEB->서버] 웹에서 LED 제어 명령 수신: {message}")
    l = message.get('data')
    
    if l == "ON":
        
        emit('led_control', 'ON', broadcast=True) 
        print("➡️ [서버->ESP32] LED ON 명령 전송 완료!")
    elif l == "OFF":   
        emit('led_control', 'OFF', broadcast=True)
        print("➡️ [서버->ESP32] LED OFF 명령 전송 완료!")
        
@socketio.on('events')
def getevents(message):
    
    print(f"🌡️ [ESP32->서버] 센서 데이터 수신: {message}")
    
    emit('dht_chart', {'data': message}, room='WEB')  
    
@socketio.on_error()
def error_handler(e):
    print('🚨 에러 발생: ' + str(e))

@app.route('/dhtchart')        
def dht_chart():
    return render_template("dhtchart.html")

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000)