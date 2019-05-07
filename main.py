import logging
import os

import gridfs
import pymongo
from flask import Flask, render_template, session
from flask_socketio import SocketIO, join_room

import chatbot_model as re
import cosine_similarity as cs

c_s = cs.Similarity()
chatbot = re.ChatBot()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)
connection = pymongo.MongoClient()


@app.before_request  # html 호출전 초기화ㅇ
def before_request():
    session['room'] = os.urandom(24)
    session['name'] = '고객'


@app.route("/", methods=['GET', 'POST'])  # 초기 화면 연결
def index():
    name = session.get('name', '')
    room = session.get('room', '')
    return render_template('chat.html', name=name, room=room)


@app.route('/download/<name>')
def downloadFile(name=None):  # pdf 다운
    fs = gridfs.GridFS(connection.Product)
    if name is not None:
        thing = fs.get_last_version(name)
        r = app.response_class(thing, direct_passthrough=True, mimetype='application/octet-stream')
        r.headers.set('Content-Disposition', 'attachment', filename=name)
        return r

# 서버 클라이언트 연결
# 연결되면 전송되는 메시지
@socketio.on('joined')
def joined(msg):
    room=session.get('room', '')
    join_room(room)
    socketio.emit('slot', {'data': '새마을금고 고객센터에 오신것을 환영합니다. \n궁금하신 항목을 선택하거나, 간단한 문장을 입력해주세요.',
                           'slots': ['상품 소개', '지점 안내', '자주 묻는 키워드', '상품 추천','테스트']}, room=room)


@socketio.on('serverFaq')  # faq 질문 처리
def server_faq_function(msg):
    room = session.get('room')
    '''
    문장간에 유사도를 측정해서 화면에 띄운다.
    '''
    question, answer = c_s.get_contents(msg)
    dataA = []
    dataB = []
    for a, b in zip(question,answer):
        dataA.append(a)
        dataB.append(b)
    if len(dataA) == 0:
        socketio.emit('messageClient', {'data': msg}, room=room)
        socketio.emit('messageServer', {'data': '검색된 데이터가 없습니다. 다시 입력해주세요.'}, room=room)
    else:
        socketio.emit('messageClient', {'data': msg}, room=room)
        socketio.emit('faq_server', {'data': '현재 FAQ 질의 공간입니다. 처음화면으로 돌아가고 싶으시면 처음화면 버튼을 눌러주세요.',
                                     'faq_db_question': dataA,'faq_db_answer': dataB}, room=room)


@socketio.on('serverMsg')  # 고객으로부터 메시지를 받으면 처리 후 다시 고객에게 메시지 전달
def server_msg_function(msg):
    room = session.get('room')
    pdf_download_check = False  # pdf 다운 생성
    faq_check = msg[:9]
    print('문자열 확인 ' + faq_check)
    if msg == '메인화면':
        socketio.emit('messageClient', {'data': '메인화면'}, room=room)
        socketio.emit('slot', {'data': '새마을금고 고객센터에 오신것을 환영합니다. \n궁금하신 항목을 선택하거나, 간단한 문장을 입력해주세요.',
                               'slots': ['상품 소개', '지점 안내', '자주 묻는 키워드', '상품 추천','테스트']}, room=room)
    elif msg == '자주 묻는 키워드':
        socketio.emit('messageClient', {'data': msg}, room=room)
        socketio.emit('faq_slot', {'data': '현재 FAQ 질의 공간입니다. 처음화면으로 돌아가고 싶으시면 처음화면 버튼을 눌러주세요.'})

    elif msg == '테스트':
        intent_data=[]
        entity_data=[]
        intent_data=['aaa','bbb','ccc']     #인텐트 데이터
        entity_data=[[1,2,3,4],[5,6,7,8],[341,132,1424,'asd']]
        socketio.emit('convergent',{'data':'테스트입니다.','intent':intent_data,'entity':entity_data},room=room)

    ################## 모델 돌린다.
    else:  # 딥러닝 모델 실행
        answer, slot = chatbot.run(msg)


        if slot.intent == "상품 소개":
            socketio.emit('messageClient',{'data': msg},room=room)
            socketio.emit('slot', {'data': answer, 'slots': slot.button}, room=room)

        elif slot.intent == "지점 안내":
            socketio.emit('messageClient', {'data': msg}, room=room)
            if slot.address.answer_find:
                socketio.emit('messageServerLocation', {'data': answer + " 새마을금고"}, room=room)
            else:
                socketio.emit('slot', {'data': '아래 항목 중에서 선택해주세요.', 'slots': slot.button}, room=room)

        elif slot.intent == "상품 추천":
             print(slot.button, slot.button_list)
             socketio.emit('messageClient', {'data': msg}, room=room)
             socketio.emit('product_recommend',{'data':answer,'data_btn': slot.button, 'data_list': slot.button_list}, room=room)


        elif slot.intent == "UnKnown":
            socketio.emit('messageClient', {'data': msg}, room=room)
            socketio.emit('messageServer', {'data': answer}, room=room)

# 클라이언트에 메시지 보낼 때 클라이언트 메시지 먼저 전송 후 서버 메시지 전송
# db 조회후 상품에 관련된 url 주소를 넘겨주면 된다.
        if pdf_download_check is True:  # pdf 약관 다운 받는 조건문
            socketio.emit('pdf_download', {'data': msg}, room=room)


if __name__ == '__main__':
    mylogger = logging.getLogger("새마을금고")
    mylogger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime) - %(name)s - %(levelname)s - %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    mylogger.addHandler(stream_handler)

    mylogger.info("server start!!")

    socketio.run(app, debug=True, use_reloader=False)