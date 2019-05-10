$(document).ready(function() {
var static_faq=false;
$('.bxslider').bxSlider();

    var socket = io.connect('http://127.0.0.1:5000');

    /////////////////////// 서버 접속  /////////////////////////////
    socket.on('connect',function(){
        socket.emit('joined',{});
    });
    /////////////////////// 서버 메시지  /////////////////////////////
    socket.on('messageServer', function(msg) {
        $(".chat").append( "<li class='left clearfix'><span class='chat-img pull-left'><img src='http://placehold.it/50/55C1E7/fff&text=BOT' alt='User Avatar' class='img-circle' /></span><div class='chat-body clearfix'><div class='header'> <strong class='primary-font'>뉴빌리지 봇</strong></div><pre>"+msg.data+"</pre></div></li>");
        $(".panel-body").scrollTop($(".chat").height());
    });

    /////////////////////// 클라이언트 접속  /////////////////////////////
    socket.on('messageClient',function(msg){
        $(".chat").append( "<li class='right clearfix'><span class='chat-img pull-right'><img src='http://placehold.it/50/55C1E7/fff&text=U' alt='User Avatar' class='img-circle' /></span><div class='chat-body clearfix'><div class='header'> <strong class='pull-right primary-font'>고객님</strong></div><br/><p style='text-align:right;'>"+msg.data+"</p></div></li>");
        $(".panel-body").scrollTop($(".chat").height());
    });

    /////////////////////// 키워드 지도   /////////////////////////////
   socket.on('messageServerLocation',function(msg){
        $(".chat").append( "<li class='left clearfix'><span class='chat-img pull-left'><img src='http://placehold.it/50/55C1E7/fff&text=BOT' alt='User Avatar' class='img-circle' /></span><div class='chat-body clearfix'><div class='header'> <strong class='primary-font'>뉴빌리지 봇</strong></div><p>"+msg.data+"</p></div></li>");

        var map_wrap=document.createElement('div');
        map_wrap.setAttribute('class','map_wrap');

        var mapMake=document.createElement('div');
        var id_value=Math.random();
        mapMake.setAttribute('id',id_value);
        mapMake.setAttribute('style',"width:100%;height:100%;position:relative;overflow:hidden;");
        map_wrap.append(mapMake);

        var menu_wrap=document.createElement('div');
        menu_wrap.setAttribute('id','menu_wrap');
        menu_wrap.setAttribute('class','bg_white');
        var option=document.createElement('div');
        option.setAttribute('class','option');
        var div_btn_text=document.createElement('div');
        div_btn_text.setAttribute('id','text_btn');
        var input_text=document.createElement('input');
        input_text.setAttribute('type','text');
        //테스트
        input_text.addEventListener("keypress",keyevent,false);
        //
        input_text.setAttribute('value',msg.data);
        var keyword_value=Math.random();
        input_text.setAttribute('id',keyword_value);
        var input_btn=document.createElement('button');
        input_btn.setAttribute('type','submit');
        input_btn.append('검색하기');
        div_btn_text.append(input_text);
        div_btn_text.append(input_btn);
        option.append(div_btn_text);
        menu_wrap.append(option);

        var hr=document.createElement('hr');
        menu_wrap.append(hr);

        var placeList=document.createElement('ul');
        var place_random=Math.random();
        placeList.setAttribute('id',place_random);
        menu_wrap.append(placeList);

        var pagination=document.createElement('div');
        var pagination_random=Math.random();
        pagination.setAttribute('id',pagination_random);
        pagination.setAttribute('style','margin:10px auto;text-align: center');
        menu_wrap.append(pagination);

        map_wrap.append(menu_wrap);

        $(".chat").append(map_wrap);


        $(".panel-body").scrollTop($(".chat").height());


        function keyevent(){
            if(event.keyCode=='13'){
                searchPlaces();
            }
        }

        $("div").on("click", "button", function(){
            searchPlaces();
        });

      // 마커를 담을 배열입니다
    var markers = [];

    var mapContainer = document.getElementById(id_value), // 지도를 표시할 div
        mapOption = {
            center: new daum.maps.LatLng(37.566826, 126.9786567), // 지도의 중심좌표
            level: 3 // 지도의 확대 레벨
        };

    // 지도를 생성합니다
    var map = new daum.maps.Map(mapContainer, mapOption);

    // 장소 검색 객체를 생성합니다
    var ps = new daum.maps.services.Places();

    // 검색 결과 목록이나 마커를 클릭했을 때 장소명을 표출할 인포윈도우를 생성합니다
    var infowindow = new daum.maps.InfoWindow({zIndex:1});


    // 키워드로 장소를 검색합니다
    searchPlaces();

    // 키워드 검색을 요청하는 함수입니다
    function searchPlaces() {

        var keyword = document.getElementById(keyword_value).value;

        if (!keyword.replace(/^\s+|\s+$/g, '')) {
            alert('키워드를 입력해주세요!');
            return false;
        }

        // 장소검색 객체를 통해 키워드로 장소검색을 요청합니다
        ps.keywordSearch( keyword, placesSearchCB);
    }

    // 장소검색이 완료됐을 때 호출되는 콜백함수 입니다
    function placesSearchCB(data, status, pagination) {
        if (status === daum.maps.services.Status.OK) {

            // 정상적으로 검색이 완료됐으면
            // 검색 목록과 마커를 표출합니다
            displayPlaces(data);

            // 페이지 번호를 표출합니다
            displayPagination(pagination);

        } else if (status === daum.maps.services.Status.ZERO_RESULT) {

            alert('검색 결과가 존재하지 않습니다.');
            return;

        } else if (status === daum.maps.services.Status.ERROR) {

            alert('검색 결과 중 오류가 발생했습니다.');
            return;

        }
    }

    // 검색 결과 목록과 마커를 표출하는 함수입니다
    function displayPlaces(places) {

        var listEl = document.getElementById(place_random),
        menuEl = document.getElementById('menu_wrap'),
        fragment = document.createDocumentFragment(),
        bounds = new daum.maps.LatLngBounds(),
        listStr = '';

        // 검색 결과 목록에 추가된 항목들을 제거합니다
        removeAllChildNods(listEl);

        // 지도에 표시되고 있는 마커를 제거합니다
        removeMarker();

        for ( var i=0; i<places.length; i++ ) {

            // 마커를 생성하고 지도에 표시합니다
            var placePosition = new daum.maps.LatLng(places[i].y, places[i].x),
                marker = addMarker(placePosition, i),
                itemEl = getListItem(i, places[i]); // 검색 결과 항목 Element를 생성합니다

            // 검색된 장소 위치를 기준으로 지도 범위를 재설정하기위해
            // LatLngBounds 객체에 좌표를 추가합니다
            bounds.extend(placePosition);

            // 마커와 검색결과 항목에 mouseover 했을때
            // 해당 장소에 인포윈도우에 장소명을 표시합니다
            // mouseout 했을 때는 인포윈도우를 닫습니다
            (function(marker, title) {
                daum.maps.event.addListener(marker, 'mouseover', function() {
                    displayInfowindow(marker, title);
                });

                daum.maps.event.addListener(marker, 'mouseout', function() {
                    infowindow.close();
                });

                itemEl.onmouseover =  function () {
                    displayInfowindow(marker, title);
                };

                itemEl.onmouseout =  function () {
                    infowindow.close();
                };
            })(marker, places[i].place_name);

            fragment.appendChild(itemEl);
        }

        // 검색결과 항목들을 검색결과 목록 Elemnet에 추가합니다
        listEl.appendChild(fragment);
        menuEl.scrollTop = 0;

        // 검색된 장소 위치를 기준으로 지도 범위를 재설정합니다
        map.setBounds(bounds);
    }

    // 검색결과 항목을 Element로 반환하는 함수입니다
    function getListItem(index, places) {

        var el = document.createElement('li'),
        itemStr = '<span class="markerbg marker_' + (index+1) + '"></span>' +
                    '<div class="info">' +
                    '   <h5>' + places.place_name + '</h5>';

        if (places.road_address_name) {
            itemStr += '    <span>' + places.road_address_name + '</span>' +
                        '   <span class="jibun gray">' +  places.address_name  + '</span>';
        } else {
            itemStr += '    <span>' +  places.address_name  + '</span>';
        }

          itemStr += '  <span class="tel">' + places.phone  + '</span>' +
                    '</div>';

        el.innerHTML = itemStr;
        el.className = 'item';

        return el;
    }

    // 마커를 생성하고 지도 위에 마커를 표시하는 함수입니다
    function addMarker(position, idx, title) {
        var imageSrc = 'http://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_number_blue.png', // 마커 이미지 url, 스프라이트 이미지를 씁니다
            imageSize = new daum.maps.Size(36, 37),  // 마커 이미지의 크기
            imgOptions =  {
                spriteSize : new daum.maps.Size(36, 691), // 스프라이트 이미지의 크기
                spriteOrigin : new daum.maps.Point(0, (idx*46)+10), // 스프라이트 이미지 중 사용할 영역의 좌상단 좌표
                offset: new daum.maps.Point(13, 37) // 마커 좌표에 일치시킬 이미지 내에서의 좌표
            },
            markerImage = new daum.maps.MarkerImage(imageSrc, imageSize, imgOptions),
                marker = new daum.maps.Marker({
                position: position, // 마커의 위치
                image: markerImage
            });

        marker.setMap(map); // 지도 위에 마커를 표출합니다
        markers.push(marker);  // 배열에 생성된 마커를 추가합니다

        return marker;
    }

    // 지도 위에 표시되고 있는 마커를 모두 제거합니다
    function removeMarker() {
        for ( var i = 0; i < markers.length; i++ ) {
            markers[i].setMap(null);
        }
        markers = [];
    }

    // 검색결과 목록 하단에 페이지번호를 표시는 함수입니다
    function displayPagination(pagination) {
        var paginationEl = document.getElementById(pagination_random),
            fragment = document.createDocumentFragment(),
            i;

        // 기존에 추가된 페이지번호를 삭제합니다
        while (paginationEl.hasChildNodes()) {
            paginationEl.removeChild (paginationEl.lastChild);
        }

        for (i=1; i<=pagination.last; i++) {
            var el = document.createElement('a');
            el.href = "#";
            el.innerHTML = i;

            if (i===pagination.current) {
                el.className = 'on';
            } else {
                el.onclick = (function(i) {
                    return function() {
                        pagination.gotoPage(i);
                    }
                })(i);
            }

            fragment.appendChild(el);
        }
        paginationEl.appendChild(fragment);
    }

    // 검색결과 목록 또는 마커를 클릭했을 때 호출되는 함수입니다
    // 인포윈도우에 장소명을 표시합니다
    function displayInfowindow(marker, title) {
        var content = '<div style="padding:5px;z-index:1;">' + title + '</div>';

        infowindow.setContent(content);
        infowindow.open(map, marker);
    }

     // 검색결과 목록의 자식 Element를 제거하는 함수입니다
    function removeAllChildNods(el) {
        while (el.hasChildNodes()) {
            el.removeChild (el.lastChild);
        }
    }
});

    /////////////////////// pdf 다운로드  /////////////////////////////
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

    /////////////////////// 버튼 생성  /////////////////////////////
    socket.on('slot',function(msg){
        $(".chat").append( "<li class='left clearfix'><span class='chat-img pull-left'><img src='http://placehold.it/50/55C1E7/fff&text=BOT' alt='User Avatar' class='img-circle' /></span><div class='chat-body clearfix'><div class='header'> <strong class='primary-font'>뉴빌리지 봇</strong></div><pre>"+msg.data);
            for(var i=0;i<msg.slots.length;i+=5){
                var div_wrap=document.createElement('div');
                div_wrap.setAttribute('id','div_wrap');
                for(var j=i;j<msg.slots.length&&j<(i+5);j++){
                    var btn=document.createElement('input');
                    btn.setAttribute('type','button');
                    btn.setAttribute('id',msg.slots[j]);
                    btn.setAttribute('value',msg.slots[j]);
                    div_wrap.append(btn);
                 }
                $(".chat").append(div_wrap);
            }
            $(".chat").append("</pre></div></li>");
            $(".panel-body").scrollTop($(".chat").height());
            $("input").click(function(){
            var text=$(this).attr('value');
            if(text!=null){
                    static_faq=false;
                    if(text=="상품 추천"){
                        socket.emit("serverMsg","추천");
                    }else{
                        socket.emit("serverMsg",text);
                    }
            }
        });
    });

    /////////////////////// 상품 추천  /////////////////////////////
    socket.on('product_recommend',function(msg){
            $(".chat").append( "<li class='left clearfix'><span class='chat-img pull-left'><img src='http://placehold.it/50/55C1E7/fff&text=BOT' alt='User Avatar' class='img-circle' /></span><div class='chat-body clearfix'><div class='header'> <strong class='primary-font'>뉴빌리지 봇</strong></div><pre>"+msg.data+"</pre>");
            for(var i=0;i<msg.data_btn.length;i++){
                var btn=document.createElement('input');
                btn.setAttribute('type','button');
                btn.setAttribute('id',msg.data_btn[i]);
                btn.setAttribute('value',msg.data_btn[i]);
                $(".chat").append(btn);
            }
            $(".chat").append("</p></div></li>");
            $(".panel-body").scrollTop($(".chat").height());
            $("input").click(function(){
            var text=$(this).attr('value');
            if(text!=null){
                    static_faq=false;
                    for(var i=0;i<msg.data_list.length;i++){
                        if(text==msg.data_list[i][0]){
                            socket.emit("serverMsg",msg.data_list[i][1]);
                            break;
                        }
                    }
            }
        });
    });

    /////////////////////// 컨버전트  /////////////////////////////
    socket.on('convergent',function(msg){
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

           var div_card=document.createElement('div');
           div_card.setAttribute('class','card');
           div_card.setAttribute('style','border:1px solid black');

           var div_header=document.createElement('div');
           div_header.setAttribute('class','card-header');
           div_header.append('질문 등록 창');

           div_card.append(div_header);

           //card 몸에 버튼 붙이기
           var div_body=document.createElement('div');
           div_body.setAttribute('class','card-body');

           var div_intent_group=document.createElement('div');
           div_intent_group.setAttribute('class','form-group row');

           var label_title=document.createElement('div');
           label_title.setAttribute('class','col-md-4 col-form-label text-md-right');
           label_title.append('의도');
           div_intent_group.append(label_title);

           var div_button=document.createElement('div');
           div_button.setAttribute('class','col-md-6');

           for(var i=0;i<msg.intent.length;i++){
                var btn=document.createElement('input');
                btn.setAttribute('type','button');
                btn.setAttribute('id',msg.intent[i]);
                value+=msg.intent[i];
                btn.setAttribute('value',msg.intent[i]);
                div_button.append(btn);
           }
           div_intent_group.append(div_button);
           div_body.append(div_intent_group);
           div_card.append(div_body);

            var div_entity_frame=document.createElement('div');

            for(var i=0;i<msg.entity.length;i++){
                var div_entity_group=document.createElement('div');
               div_entity_group.setAttribute('class','form-group row');

               var label_title=document.createElement('div');
               label_title.setAttribute('class','col-md-4 col-form-label text-md-right');
               label_title.append("entity "+(i+1)+" : ");
               div_entity_group.append(label_title);

               var div_button=document.createElement('div');
               div_button.setAttribute('class','col-md-6');

                for(var j=0;j<msg.entity[i].length;j++){
                    var btn=document.createElement('input');
                    btn.setAttribute('type','button');
                    btn.setAttribute('id',msg.entity[i][j]);
                    btn.setAttribute('value',msg.entity[i][j]);
                    value+=msg.entity[i][j];
                    div_entity_group.append(btn);
                 }
                 div_entity_frame.append(div_entity_group);
            }
           div_body.append(div_entity_frame);
           div_card.append(div_body);


           var div_add_clear_btn=document.createElement('div');
           div_add_clear_btn.setAttribute('style','text-align:right; margin-right:5px; margin-bottom:5px');
           //추가 버튼
           var div_inner_addBtn=document.createElement('input');
           div_inner_addBtn.setAttribute('type','button');
           div_inner_addBtn.setAttribute('id','innerAddBtn');
           div_inner_addBtn.setAttribute('value','추가')
           div_inner_addBtn.setAttribute('style','background-color:gray');

           div_add_clear_btn.append(div_inner_addBtn);

           //취소 버튼
           var div_inner_clearBtn=document.createElement('input');
           div_inner_clearBtn.setAttribute('type','button');
           div_inner_clearBtn.setAttribute('id','innerClearBtn');
           div_inner_clearBtn.setAttribute('value','취소')
           div_inner_clearBtn.setAttribute('style','background-color:gray');
           div_add_clear_btn.append(div_inner_clearBtn);

           div_card.append(div_add_clear_btn);
           div_frame.append(div_card);

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

    /////////////////////// faq  /////////////////////////////
    socket.on('faq_slot',function(msg){
         static_faq=true;
        $(".chat").append( "<li class='left clearfix'><span class='chat-img pull-left'><img src='http://placehold.it/50/55C1E7/fff&text=BOT' alt='User Avatar' class='img-circle' /></span><div class='chat-body clearfix'><div class='header'> <strong class='primary-font'>뉴빌리지 봇</strong></div><p>"+msg.data);
            $(".chat").append("</p></div></li>");
            $(".panel-body").scrollTop($(".chat").height());
    });

    /////////////////////// faq 접속  /////////////////////////////
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


    /////////////////////// 메인화면 버튼  /////////////////////////////
    $('#returnBtn').on('click',function(){
        static_faq=false;
        socket.emit("serverMsg","메인화면");
    });

    /////////////////////// 전송 버튼  /////////////////////////////
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

    /////////////////////// 엔터 키 이벤트  /////////////////////////////
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

