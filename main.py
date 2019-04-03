import os
from flask import Flask, render_template,session,session,redirect,url_for,request
from flask_socketio import SocketIO,emit,join_room,leave_room
import logging
import chatbot_model as re
import gridfs
import pymongo

print(1234)
chatbot=re.ChatBot()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)
connection = pymongo.MongoClient()
#html 호출전 초기화
@app.before_request
def before_request():
    session['room']=os.urandom(24)
    session['name']='고객'

#초기 화면 연결
@app.route("/",methods=['GET','POST'])
def index():
    name=session.get('name','')
    room=session.get('room','')
    return render_template('chat.html',name=name,room=room)


#pdf 다운
@app.route('/download/<name>')
def downloadFile(name=None):
    fs = gridfs.GridFS(connection.Product)

    if name is not None:
        thing = fs.get_last_version(name)

        r = app.response_class(thing, direct_passthrough=True, mimetype='application/octet-stream')

        r.headers.set('Content-Disposition', 'attachment', filename=name)

        return r

#서버 클라이언트 연결
#연결되면 전송되는 메시지
@socketio.on('joined')
def joined(msg):
    room=session.get('room','')
    join_room(room)
    socketio.emit('init',{'data':'새마을금고 고객센터에 오신것을 환영합니다. 궁금하신 항목을 선택하거나, 간단한 문장을 입력해주세요.' },room=room)


#고객으로부터 메시지를 받으면 처리 후 다시 고객에게 메시지 전달
@socketio.on('serverMsg')
def server_msg_function(msg):
    room=session.get('room')

    slotfilling=False         #버튼 생성
    branch_information=False     #지도 생성
    pdf_download_check=False    #pdf 다운 생성
    branch_information=False


    intentData, _= chatbot.run(msg)
    print("지점안내 : "+intentData)

    if intentData[-5:] == '새마을금고':
        branch_information = True

    #모델 돌려서 슬롯필링으로 처리할지 그냥 넘길지 판단 후

    ##클라이언트에 메시지 보낼 때 클라이언트 메시지 먼저 전송 후 서버 메시지 전송
    #db 조회후 상품에 관련된 url 주소를 넘겨주면 된다.
    #기본 메시지 전달
    if slotfilling==False and branch_information==False:
        socketio.emit('messageClient',{'data':msg},room=room)
        socketio.emit('messageServer',{'data':intentData},room=room)

    # 슬롯필링 버튼 여러개 생성하는 조건문
    elif slotfilling==True and branch_information==False:
        socketio.emit('messageClient',{'data':msg},room=room)

        arr=['상품안내', '지점안내', 'FAQ']
        socketio.emit('slot',{'data':'아래 항목 중에서 선택해주세요.','slots':arr},room=room)

    #지점안내 지도 그려지는 조건문 (키워드가 주어지면 그 키워드에 맞는 지도를 출력해주면 된다.)

    if branch_information==True and slotfilling==False:
        socketio.emit('messageClient',{'data':msg},room=room)
        socketio.emit('messageServerLocation',{'data':intentData},room=room)

    #pdf 약관 다운 받는 조건문
    if pdf_download_check==True:
        socketio.emit('pdf_download',{'data':msg},room=room)

if __name__ == '__main__':
    mylogger=logging.getLogger("새마을금고")
    mylogger.setLevel(logging.INFO)
    formatter=logging.Formatter('%(asctime) - %(name)s - %(levelname)s - %(message)s')
    stream_handler=logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    mylogger.addHandler(stream_handler)

    mylogger.info("server start!!")

    socketio.run(app,debug=True, use_reloader=False)
