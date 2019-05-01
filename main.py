import logging
import os

import gridfs
import pymongo
from flask import Flask, render_template, session
from flask_socketio import SocketIO, join_room

import chatbot_model as re
import cosine_similarity as cs

c_s=cs.Similarity()
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
    socketio.emit('slot',{'data':'새마을금고 고객센터에 오신것을 환영합니다. \n궁금하신 항목을 선택하거나, 간단한 문장을 입력해주세요.','slots':['상품 소개','지점 안내','자주 묻는 키워드','상품 추천'] },room=room)

#faq 질문 처리
@socketio.on('serverFaq')
def server_faq_function(msg):
    room = session.get('room')
    '''
    문장간에 유사도를 측정해서 화면에 띄운다.
    '''
    question, answer = c_s.get_contents(msg)
    dataA=[]
    dataB=[]
    for a,b in zip(question,answer):
        dataA.append(a)
        dataB.append(b)

    socketio.emit('messageClient', {'data': msg}, room=room)
    socketio.emit('faq_server', {'data': '현재 FAQ 질의 공간입니다. 처음화면으로 돌아가고 싶으시면 처음화면 버튼을 눌러주세요.','slots': ['전체보기', '대출', '인터넷뱅킹', '예금'],
                                             'faq_db_question':dataA,'faq_db_answer':dataB},
                              room=room)


#고객으로부터 메시지를 받으면 처리 후 다시 고객에게 메시지 전달
@socketio.on('serverMsg')
def server_msg_function(msg):
    room=session.get('room')

    pdf_download_check=False    #pdf 다운 생성

    faq_check=msg[:9]
    print('문자열 확인 '+faq_check)
    if msg == '메인화면':
        socketio.emit('messageClient', {'data': '메인화면'}, room=room)
        socketio.emit('slot', {'data': '새마을금고 고객센터에 오신것을 환영합니다. \n궁금하신 항목을 선택하거나, 간단한 문장을 입력해주세요.',
                               'slots': ['상품 소개', '지점 안내', '자주 묻는 키워드', '상품 추천'],
                               }, room=room)
    elif faq_check=='자주 묻는 키워드':
        if len(msg) != 9:
            select_faq = msg[10:]
            #여기서 db에 저장된 데이터들을 꺼내온다..

            if select_faq == '전체보기':
                socketio.emit('messageClient',{'data':select_faq},room=room)        #클라이언트 메시지
                #전체보기인 경우 데이터들 전부 출력
                socketio.emit('faq_server',{'data':'전체보기 FAQ 입니다. \n 찾고자 하는 키워드를 입력해주세요.','slots': ['전체보기', '대출', '인터넷뱅킹', '예금'],'faq_db':['1','2','3','4','5','6','7','8']},room=room)    #디비에서 모든 질
                #해당되는 질문 & 답을 전부 출력하면 된다.
            elif select_faq == '예금':
                socketio.emit('messageClient', {'data': select_faq}, room=room)  # 클라이언트 메시지
                #예금인 경우 예금 데이터들 전부 출력
                socketio.emit('faq_server',{'data': '예적금 FAQ 입니다. \n 찾고자 하는 키워드를 입력해주세요. ','slots': ['전체보기', '대출', '인터넷뱅킹', '예금'],'faq_db': ['1', '2', '3', '4', '5', '6', '7', '8']},room=room)  # 디비에서 모든 질
            elif select_faq == '인터넷뱅킹':
                socketio.emit('messageClient', {'data': select_faq}, room=room)  # 클라이언트 메시지
                #인터넷뱅킹인 경우 인터넷 뱅킹 데이터 전부 출력
                socketio.emit('faq_server', {'data': '인터넷뱅킹 FAQ 입니다. \n 찾고자 하는 키워드를 입력해주세요. ',
                                             'slots': ['전체보기', '대출', '인터넷뱅킹', '예금'],
                                             'faq_db': ['1', '2', '3', '4', '5', '6', '7', '8']},
                              room=room)  # 디비에서 모든 질
            elif select_faq == '대출':
                socketio.emit('messageClient', {'data': select_faq}, room=room)  # 클라이언트 메시지
                socketio.emit('faq_server', {'data': '대출 FAQ 입니다. \n 찾고자 하는 키워드를 입력해주세요. ',
                                             'slots': ['전체보기', '대출', '인터넷뱅킹', '예금'],
                                             'faq_db': ['1', '2', '3', '4', '5', '6', '7', '8']},
                              room=room)  # 디비에서 모든 질

        else:   #초기화면
            socketio.emit('messageClient', {'data': msg}, room=room)
            socketio.emit('faq_slot', {'data': '궁금한 키워드를 입력해주세요..', 'slots': ['전체보기', '대출', '인터넷뱅킹', '예금']},
                          room=room)

    ################## 모델 돌린다.
    else :
        answer, slot= chatbot.run(msg)

        if slot.intent == "상품 소개":
            socketio.emit('messageClient',{'data':msg},room=room)
            socketio.emit('slot',{'data':'아래 항목 중에서 선택해주세요.','slots':slot.button},room=room)

        elif slot.intent == "지점 안내":
            socketio.emit('messageClient',{'data':msg},room=room)
            if slot.address.answer_find:
                socketio.emit('messageServerLocation', {'data': answer}, room=room)
            else:
                socketio.emit('messageServer',{'data':answer},room=room)

        elif slot.intent == "고객 상담":
            pass

        elif slot.intent == "상품 추천":
            pass


        ##클라이언트에 메시지 보낼 때 클라이언트 메시지 먼저 전송 후 서버 메시지 전송
        #db 조회후 상품에 관련된 url 주소를 넘겨주면 된다.
        #기본 메시지 전달

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
