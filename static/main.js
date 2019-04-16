$(document).ready(function() {
    var socket = io.connect('http://127.0.0.1:5000');
    socket.on('connect',function(){
        socket.emit('joined',{});
    });
    socket.on('messageServer', function(msg) {
        $(".chat").append( "<li class='left clearfix'><span class='chat-img pull-left'><img src='http://placehold.it/50/55C1E7/fff&text=BOT' alt='User Avatar' class='img-circle' /></span><div class='chat-body clearfix'><div class='header'> <strong class='primary-font'>뉴빌리지 봇</strong></div><p>"+msg.data+"</p></div></li>");
        $(".panel-body").scrollTop($(".chat").height());
    });
    socket.on('messageClient',function(msg){
        $(".chat").append( "<li class='right clearfix'><span class='chat-img pull-right'><img src='http://placehold.it/50/55C1E7/fff&text=U' alt='User Avatar' class='img-circle' /></span><div class='chat-body clearfix'><div class='header'> <strong class='pull-right primary-font'>고객님</strong></div> <p>"+msg.data+"</p></div></li>");
        $(".panel-body").scrollTop($(".chat").height());
    });

    socket.on('messageServerLocation',function(msg){
        $(".chat").append( "<li class='left clearfix'><span class='chat-img pull-left'><img src='http://placehold.it/50/55C1E7/fff&text=BOT' alt='User Avatar' class='img-circle' /></span><div class='chat-body clearfix'><div class='header'> <strong class='primary-font'>뉴빌리지 봇</strong></div><p>"+msg.data+"</p></div></li>");
        var mapMake=document.createElement('div');
        var id_value=Math.random();
        mapMake.setAttribute('id',id_value);
        mapMake.setAttribute('style',"width:300px;height:300px;");
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
            socket.emit("serverMsg",text);
        });
    });

    socket.on('faq_slot',function(msg){
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
            socket.emit("serverMsg",'자주 묻는 키워드@'+text);
        });
    });
    //입력 콜백함수
    $('#inputBtn').on('click',function(){
    socket.emit("serverMsg",$('#myMessage').val());
    $('#myMessage').val('');
    });

    $('#myMessage').keypress(function(e) {
        var code = e.keyCode || e.which;
        if (code == 13) {
            text = $('#myMessage').val();
            $('#myMessage').val('');
            socket.emit("serverMsg",text);
        }
    });
    });
    function make(){
        container.style.display="none";
        var img = document.createElement('img'); // 이미지 객체 생성
        img.onclick = function(){document.getElementById('board').removeChild(this)}; // 이미지를 클릭하면 제거되는 onclick 함수 생성
        img.src = 'https://scontent-icn1-1.xx.fbcdn.net/v/t1.0-9/16641049_625376667647811_8844539678282274552_n.png?_nc_cat=103&_nc_ht=scontent-icn1-1.xx&oh=55d1f745fa762e5fbc966898ea7be6d0&oe=5D0A450D'
        img.style.cursor = 'pointer'; // 커서 지정
        img.style.width="40px";
        img.style.height="40px";
        document.getElementById('board').appendChild(img); // board DIV 에 이미지 동적 추가
    }

    function del(){
    container.style.display="";
    document.getElementById('board').innerHTML = '';
    }


    $('#blogCarousel').carousel({
    interval: 5000
});