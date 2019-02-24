import os
from flask import Flask, render_template,session
from flask_socketio import SocketIO, send,emit
import logging
import retrieval_model as re

chatbot = re.ChatBot()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)

#html 호출전 초기화
@app.before_request
def before_request():
    if 'session' in session and 'user-id' in session:
        pass
    else:
        session['session']=os.urandom(24)
        session['username']='고객'

#초기 화면 연결
@app.route("/",methods=['GET','POST'])
def index():
    return render_template('chat.html')

#연결 됨
@socketio.on('connect')
def connect():
    emit("init", {'data': '새마을 금고에 오신것을 환영합니다. 무엇이 궁금하신가요?', 'username': '뉴빌리지봇'})


#요청을 받는다
@socketio.on('request')
def request(message):
    emit('response', {'data': message['data'], 'username': session['username']})
    emit('botResponse', {'data': chatbot.run(message['data']), 'username': '뉴빌리지봇'})               #봇 응답 보내기
    mylogger.info(message)


if __name__ == '__main__':
    mylogger = logging.getLogger("새마을금고")
    mylogger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    mylogger.addHandler(stream_handler)

    mylogger.info("server start!!")

    socketio.run(app,debug=True)
