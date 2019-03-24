import os
from flask import Flask, render_template,session
from flask_socketio import SocketIO
import logging
import retrieval_model as re


chatbot=re.ChatBot()
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

#연결되면 전송되는 메시지
@socketio.on('connect')
def initMsg():
    socketio.emit('init',{'data':'새마을금고 고객센터에 오신것을 환영합니다.'})

#고객으로부터 메시지를 받으면 처리 후 다시 고객에게 메시지 전달
@socketio.on('serverMsg')
def server_msg_function(msg):
    print('client: ' + msg)
    slotfilling=False
    intentData, _, _, _, _=chatbot.run(msg)
    #모델 돌려서 슬롯필링으로 처리할지 그냥 넘길지 판단 후

    if slotfilling==False:
        socketio.emit('messageClient',{'data':msg})
        socketio.emit('messageServer',{'data':intentData})
    else:
        socketio.emit('messageClient',{'data':msg})
        arr=['대출','이자','상품','기타']
        socketio.emit('slot',{'data':arr})

if __name__ == '__main__':
    mylogger=logging.getLogger("새마을금고")
    mylogger.setLevel(logging.INFO)
    formatter=logging.Formatter('%(asctime) - %(name)s - %(levelname)s - %(message)s')
    stream_handler=logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    mylogger.addHandler(stream_handler)

    mylogger.info("server start!!")

    socketio.run(app,debug=True)
