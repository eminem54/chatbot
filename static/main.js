$(document).ready(function() {
var static_faq=false;
$('.bxslider').bxSlider();

    var socket = io.connect('http://127.0.0.1:5000');
    socket.on('connect',function(){
        socket.emit('joined',{});
    });
    socket.on('messageServer', function(msg) {
        $(".chat").append( "<li class='left clearfix'><span class='chat-img pull-left'><img src='http://placehold.it/50/55C1E7/fff&text=BOT' alt='User Avatar' class='img-circle' /></span><div class='chat-body clearfix'><div class='header'> <strong class='primary-font'>뉴빌리지 봇</strong></div><pre>"+msg.data+"</pre></div></li>");
        $(".panel-body").scrollTop($(".chat").height());
    });
    socket.on('messageClient',function(msg){
        $(".chat").append( "<li class='right clearfix'><span class='chat-img pull-right'><img src='http://placehold.it/50/55C1E7/fff&text=U' alt='User Avatar' class='img-circle' /></span><div class='chat-body clearfix'><div class='header'> <strong class='pull-right primary-font'>고객님</strong></div><br/><p style='text-align:right;'>"+msg.data+"</p></div></li>");
        $(".panel-body").scrollTop($(".chat").height());
    });

    socket.on('messageServerLocation',function(msg){
        $(".chat").append( "<li class='left clearfix'><span class='chat-img pull-left'><img src='http://placehold.it/50/55C1E7/fff&text=BOT' alt='User Avatar' class='img-circle' /></span><div class='chat-body clearfix'><div class='header'> <strong class='primary-font'>뉴빌리지 봇</strong></div><p>"+msg.data+"</p></div></li>");
        var mapMake=document.createElement('div');
        var id_value=Math.random();
        mapMake.setAttribute('id',id_value);
        mapMake.setAttribute('style',"width:100%;height:300px;");
        $(".chat").append(mapMake);
        var infowindow = new daum.maps.InfoWindow({zIndex:1});

        var mapContainer = document.getElementById(id_value), // 지도를 표시할 div
        mapOption = {
        center: new daum.maps.LatLng(37.566826, 126.9786567), // 지도의 중심좌표
        level: 1 // 지도의 확대 레벨
    };

    // 지도를 생성합니다
    var map = new daum.maps.Map(mapContainer, mapOption);
    var ps = new daum.maps.services.Places();
    // 키워드로 장소를 검색합니다
    ps.keywordSearch(msg.data, placesSearchCB);

    // 키워드 검색 완료 시 호출되는 콜백함수 입니다
    function placesSearchCB (data, status, pagination) {
        if (status === daum.maps.services.Status.OK) {

            // 검색된 장소 위치를 기준으로 지도 범위를 재설정하기위해
            // LatLngBounds 객체에 좌표를 추가합니다
            var bounds = new daum.maps.LatLngBounds();

            for (var i=0; i<data.length; i++) {
            displayMarker(data[i]);
            bounds.extend(new daum.maps.LatLng(data[i].y, data[i].x));
            }

            // 검색된 장소 위치를 기준으로 지도 범위를 재설정합니다
            map.setBounds(bounds);
        }
    }

    // 지도에 마커를 표시하는 함수입니다
    function displayMarker(place) {

        // 마커를 생성하고 지도에 표시합니다
        var marker = new daum.maps.Marker({
        map: map,
        position: new daum.maps.LatLng(place.y, place.x)
        });

        // 마커에 클릭이벤트를 등록합니다
        daum.maps.event.addListener(marker, 'click', function() {
            // 마커를 클릭하면 장소명이 인포윈도우에 표출됩니다
            infowindow.setContent('<div style="padding:5px;font-size:12px;">' + place.place_name + '</div>');
            infowindow.open(map, marker);
        });
        }
    });

    socket.on('pdf_download',function(msg){
        $(".chat").append("<li>"+"상품 약관 다운로드 하기 : ");
        var btn=document.createElement('input');
        btn.setAttribute('type','button');
        btn.setAttribute('id','pdf_btn');
        btn.setAttribute('value','Download');
        btn.setAttribute('onclick',"location.href='http://127.0.0.1:5000/download/sangsang2.pdf'");

        $(".chat").append(btn);
        $(".chat").append("</li>");
        $(".panel-body").scrollTop($(".chat").height());
    });
    socket.on('slot',function(msg){
        $(".chat").append( "<li class='left clearfix'><span class='chat-img pull-left'><img src='http://placehold.it/50/55C1E7/fff&text=BOT' alt='User Avatar' class='img-circle' /></span><div class='chat-body clearfix'><div class='header'> <strong class='primary-font'>뉴빌리지 봇</strong></div><p>"+msg.data);
            for(var i=0;i<msg.slots.length;i++){
                var btn=document.createElement('input');
                btn.setAttribute('type','button');
                btn.setAttribute('id',msg.slots[i]);
                btn.setAttribute('value',msg.slots[i]);
                $(".chat").append(btn);
            }
            $(".chat").append("</p></div></li>");
            $(".panel-body").scrollTop($(".chat").height());
            $("input").click(function(){
            var text=$(this).attr('value');
            if(text!=null){
                    static_faq=false;
                    socket.emit("serverMsg",text);
            }
        });
    });
    //기본 태그 설정
    /*
    socket.on('test',function(msg){
           var left_clearfix=document.createElement('li');
           left_clearfix.setAttribute('class','leftclearfix');

           var chat_img=document.createElement('span');
           chat_img.setAttribute('class',"chat-img pull-left");
           var img=document.createElement('img');
           img.setAttribute('src','http://placehold.it/50/55C1E7/fff&text=BOT');
           img.setAttribute('alt','User Avatar');
           img.setAttribute('class','img-circle');
           chat_img.appendChild(img);
           left_clearfix.appendChild(chat_img);

           var chat_body=document.createElement('div');
           chat_body.setAttribute('class','chat-body clearfix');
           var header=document.createElement('div');
           header.setAttribute('class','header');
           var primary_font=document.createElement('strong');
           primary_font.setAttribute('class','primary-font');
           primary_font.append('뉴빌리지 봇');
           header.appendChild(primary_font);
           chat_body.appendChild(header);
           var pp=document.createElement('p');
           pp.append(msg.data);



            chat_body.appendChild(pp);
           left_clearfix.appendChild(chat_body);
           $(".chat").append(left_clearfix);
           $(".chat").append(div_box[0]);
           //버튼 생성
           for(var i=0;i<msg.slots.length;i++){
                var btn=document.createElement('input');
                btn.setAttribute('type','button');
                btn.setAttribute('id',msg.slots[i]);
                btn.setAttribute('value',msg.slots[i]);
                $(".chat").append(btn);
            }


            var return_btn=document.createElement('input');
            return_btn.setAttribute('type','button');
            return_btn.setAttribute('id','returnBtn');
            return_btn.setAttribute('value','처음화면');
            $(".chat").append(return_btn);


            $(".panel-body").scrollTop($(".chat").height());
    });

    */


    //컴퍼젼트 테스트
    socket.on('test',function(msg){
           var left_clearfix=document.createElement('li');
           left_clearfix.setAttribute('class','leftclearfix');

           var chat_img=document.createElement('span');
           chat_img.setAttribute('class',"chat-img pull-left");
           var img=document.createElement('img');
           img.setAttribute('src','http://placehold.it/50/55C1E7/fff&text=BOT');
           img.setAttribute('alt','User Avatar');
           img.setAttribute('class','img-circle');
           chat_img.appendChild(img);
           left_clearfix.appendChild(chat_img);

           var chat_body=document.createElement('div');
           chat_body.setAttribute('class','chat-body clearfix');
           var header=document.createElement('div');
           header.setAttribute('class','header');
           var primary_font=document.createElement('strong');
           primary_font.setAttribute('class','primary-font');
           primary_font.append('뉴빌리지 봇');
           header.appendChild(primary_font);
           chat_body.appendChild(header);
           var pp=document.createElement('p');
           pp.append(msg.data);

           var value="";
           // 초기 프레임창 띄우기위한 버튼
           var save_btn=document.createElement('input');
           save_btn.setAttribute('type','button');
           save_btn.setAttribute('id','saveBtn');
           save_btn.setAttribute('value',"저장하기");

           pp.append(save_btn);

           //프레임창 생성
           var div_frame=document.createElement('div');
           div_frame.setAttribute('id','divSave');
           div_frame.setAttribute('style','display:none;');

           //질문 등록 창
           var div_text=document.createElement('input');
           div_text.setAttribute('type','text');
           div_text.setAttribute('id','divText');
           div_text.setAttribute('style','background-color:#F5F5F5');
           div_frame.append(div_text);


           //의도 프레임 (버튼들 생성)
           var intent_frame=document.createElement('div');
           intent_frame.append('의도');
           var space=document.createElement('br');
           intent_frame.appendChild(space);
           for(var i=0;i<msg.intent.length;i++){
                var btn=document.createElement('input');
                btn.setAttribute('type','button');
                btn.setAttribute('id',msg.intent[i]);
                value+=msg.intent[i];
                btn.setAttribute('value',msg.intent[i]);
                intent_frame.append(btn);
           }
           div_frame.append(intent_frame);

           //개체 프레임 생성 및 버튼 생성

            for(var i=0;i<msg.entity.length;i++){
                var entity_frame=document.createElement('div');
                entity_frame.append("entity "+(i+1)+" : ");
                var space=document.createElement('br');
                entity_frame.appendChild(space);
                for(var j=0;j<msg.entity[i].length;j++){
                    var btn=document.createElement('input');
                    btn.setAttribute('type','button');
                    btn.setAttribute('id',msg.entity[i][j]);
                    btn.setAttribute('value',msg.entity[i][j]);
                    value+=msg.entity[i][j];
                    entity_frame.append(btn);
                 }
                 div_frame.append(entity_frame);
            }


           //추가 버튼
           var div_inner_addBtn=document.createElement('input');
           div_inner_addBtn.setAttribute('type','button');
           div_inner_addBtn.setAttribute('id','innerAddBtn');
           div_inner_addBtn.setAttribute('value','추가')
           div_inner_addBtn.setAttribute('style','background-color:gray');
           div_frame.append(div_inner_addBtn);

           //취소 버튼
           var div_inner_clearBtn=document.createElement('input');
           div_inner_clearBtn.setAttribute('type','button');
           div_inner_clearBtn.setAttribute('id','innerClearBtn');
           div_inner_clearBtn.setAttribute('value','취소')
           div_inner_clearBtn.setAttribute('style','background-color:gray');
           div_frame.append(div_inner_clearBtn);


            pp.append(div_frame);

            $(document).on("click","#innerClearBtn",function(){
                $('#divSave').hide();
            });

            $(document).on("click","#innerAddBtn",function(){
                alert(value);

            });

            $(document).on("click","#saveBtn",function(){
                    var state=$('#divSave').css('display');
                    if(state=='none'){
                        $('#divSave').show();
                    }else{
                        $('#divSave').hide();
                    }
             });

           chat_body.appendChild(pp);
           left_clearfix.appendChild(chat_body);
           $(".chat").append(left_clearfix);
           $(".chat").append(div_box[0]);


            var return_btn=document.createElement('input');
            return_btn.setAttribute('type','button');
            return_btn.setAttribute('id','returnBtn');
            return_btn.setAttribute('value','처음화면');
            $(".chat").append(return_btn);



            $(".panel-body").scrollTop($(".chat").height());
    });
    //faq 슬롯 구현
    socket.on('faq_slot',function(msg){
         static_faq=true;
        $(".chat").append( "<li class='left clearfix'><span class='chat-img pull-left'><img src='http://placehold.it/50/55C1E7/fff&text=BOT' alt='User Avatar' class='img-circle' /></span><div class='chat-body clearfix'><div class='header'> <strong class='primary-font'>뉴빌리지 봇</strong></div><p>"+msg.data);
            $(".chat").append("</p></div></li>");
            $(".panel-body").scrollTop($(".chat").height());
    });
    //faq_server
     socket.on('faq_server',function(msg){
           static_faq=true;

           var left_clearfix=document.createElement('li');
           left_clearfix.setAttribute('class','leftclearfix');


           var chat_img=document.createElement('span');
           chat_img.setAttribute('class',"chat-img pull-left");
           var img=document.createElement('img');
           img.setAttribute('src','http://placehold.it/50/55C1E7/fff&text=BOT');
           img.setAttribute('alt','User Avatar');
           img.setAttribute('class','img-circle');
           chat_img.appendChild(img);
           left_clearfix.appendChild(chat_img);

           var chat_body=document.createElement('div');
           chat_body.setAttribute('class','chat-body clearfix');
           var header=document.createElement('div');
           header.setAttribute('class','header');
           var primary_font=document.createElement('strong');
           primary_font.setAttribute('class','primary-font');
           primary_font.append('뉴빌리지 봇');
           header.appendChild(primary_font);
           chat_body.appendChild(header);

          // 유사도 추출된 문장 출력
           var pp=document.createElement('p');
           pp.append(msg.data);
           var div_box = $("<div />");
           var faq_ul = $("<ul/ >");
               for (var i=0;i<msg.faq_db_question.length;i++){
                    var faq_li=document.createElement('li');
                    faq_li.setAttribute('style','text-align:center');
                    var faq_details=document.createElement('details');
                    var faq_question=document.createElement('summary');
                    faq_question.append(msg.faq_db_question[i]);
                    faq_details.append(faq_question);
                    var faq_answer=document.createElement('p');
                    faq_answer.append(msg.faq_db_answer[i]);
                    faq_details.append(faq_answer);
                    faq_li.append(faq_details);
                    faq_ul.append(faq_li);
               }
          div_box.append(faq_ul);
          chat_body.appendChild(pp);
           left_clearfix.appendChild(chat_body);
           $(".chat").append(left_clearfix);
           $(".chat").append(div_box[0]);
           //버튼 생성
           for(var i=0;i<msg.slots.length;i++){
                var btn=document.createElement('input');
                btn.setAttribute('type','button');
                btn.setAttribute('id',msg.slots[i]);
                btn.setAttribute('value',msg.slots[i]);
                $(".chat").append(btn);
            }


            var return_btn=document.createElement('input');
            return_btn.setAttribute('type','button');
            return_btn.setAttribute('id','returnBtn');
            return_btn.setAttribute('value','처음화면');
            $(".chat").append(return_btn);


            $(".panel-body").scrollTop($(".chat").height());

     });

    //faq_server  슬라이드
/*
    socket.on('faq_server',function(msg){
           var left_clearfix=document.createElement('li');
           left_clearfix.setAttribute('class','leftclearfix');


           var chat_img=document.createElement('span');
           chat_img.setAttribute('class',"chat-img pull-left");
           var img=document.createElement('img');
           img.setAttribute('src','http://placehold.it/50/55C1E7/fff&text=BOT');
           img.setAttribute('alt','User Avatar');
           img.setAttribute('class','img-circle');
           chat_img.appendChild(img);
           left_clearfix.appendChild(chat_img);

           var chat_body=document.createElement('div');
           chat_body.setAttribute('class','chat-body clearfix');
           var header=document.createElement('div');
           header.setAttribute('class','header');
           var primary_font=document.createElement('strong');
           primary_font.setAttribute('class','primary-font');
           primary_font.append('뉴빌리지 봇');
           header.appendChild(primary_font);
           chat_body.appendChild(header);

          // 유사도 추출된 문장 출력
           var pp=document.createElement('p');
           pp.append(msg.data);
           var slider = $("<div class='slider' />");
           var box = $("<ul class='bxslider'/>");
           for(var i=0;i<msg.faq_db_question.length;i++){
               var li=document.createElement('li');
               li.setAttribute('style','text-align:center');

               var title=document.createElement('div');
               title.append(msg.faq_db_question[i]);
               li.append(title);
               li.innerHTML='<details><summary>제목</summary><p>내용</p></details>';
               var hr=document.createElement('hr');
               li.append(hr);
               var content=document.createElement('div');
               content.append(msg.faq_db_answer[i]);
               li.append(content);
               box.append(li);
               slider.append(box);
           }
           chat_body.appendChild(pp);
           left_clearfix.appendChild(chat_body);
           $(".chat").append(left_clearfix);
           $(".chat").append(slider[0]);
           $('.bxslider').bxSlider();

           //버튼 생성
           for(var i=0;i<msg.slots.length;i++){
                var btn=document.createElement('input');
                btn.setAttribute('type','button');
                btn.setAttribute('id',msg.slots[i]);
                btn.setAttribute('value',msg.slots[i]);
                $(".chat").append(btn);
            }
            var return_btn=document.createElement('input');
            return_btn.setAttribute('type','button');
            return_btn.setAttribute('id','returnBtn');
            return_btn.setAttribute('value','처음화면');
            $(".chat").append(return_btn);


            $(".panel-body").scrollTop($(".chat").height());
            $("input").click(function(){
            static_faq=true;
            var text=$(this).attr('value');
            socket.emit("serverMsg",'자주 묻는 키워드@'+text);
        });
    });
*/


    $('#returnBtn').on('click',function(){
        static_faq=false;
        socket.emit("serverMsg","메인화면");
    });
    //입력 콜백함수
    $('#inputBtn').on('click',function(){
    if(static_faq==false){
        socket.emit("serverMsg",$('#myMessage').val());
        $('#myMessage').val('');
    }
    else{
        socket.emit("serverFaq",$('#myMessage').val());
        $('#myMessage').val('');
    }
    });
    function text_click() {
	    alert("버튼1을 누르셨습니다.");
    }
    $('#myMessage').keypress(function(e) {
    if(static_faq==false){
        var code = e.keyCode || e.which;
        if (code == 13) {
            text = $('#myMessage').val();
            $('#myMessage').val('');
            socket.emit("serverMsg",text);
        }
    }
    else{
        var code = e.keyCode || e.which;
        if (code == 13) {
            text = $('#myMessage').val();
            $('#myMessage').val('');
            socket.emit("serverFaq",text);
        }
    }
    });
 });

