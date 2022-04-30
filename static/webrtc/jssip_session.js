var ua;
var	wss_host; 
var sip_host;
var session;
var header
var text;
var fs_ip;
function sipInitialize(){
    JsSIP.debug.enable('JsSIP:*');

    var socket = new JsSIP.WebSocketInterface(websocket_proxy_url);
    
    var configuration = {
        sockets  : [ socket ],
        uri      : sip_identity,
        password : "1234",
        register : true,
    };
    ua = new JsSIP.UA(configuration);
    
    ua.start();
    
    
    navigator.mediaDevices.getUserMedia({ audio: true })
    ua.on('connected',function(e){
        console.log('connected...'+e)
        makeCall()
    });
    
    ua.on('newRTCSession', function(e){ 
        console.log('newRTC...',e)
        console.log('-----------------',e.request);
        session = e.session;
        session.on('sdp', (data) => {
            console.log("sdp------",data)
            
        })
        session.on('peerconnection',(data)=>{
            console.log("peerconnection-----",data);
        })
        session.on('newInfo',(data)=>{
            console.log("newInfo-----",data);
        })
        session.on('reinvite',(data)=>{
            console.log("reinvite-----",data);
        })
        session.on('update',(data)=>{
            console.log("update-----",data);
        })
        e.session.on('confirmed', function(e) {
            console.log('session: confirmed');
            $('.preloader').fadeOut('slow')
            
        });
    });
}


function updateheaderParam(key,value){
    header.setParam(key,value)
}
function deleteHeaderParam(key){
    header.deleteParam(key)
}

function session_hangup(){
    ua.stop();
}
function makeCall(dial_number)
{
	var options = {
        'eventHandlers'    : eventHandlers,
        'mediaConstraints' : { 'audio': true, 'video': false },
        'sessionTimersExpires' : 3600,
        'extraHeaders': [ 'X-Extension: '+extension, 'X-Bar: bar' ],
    };
    session = ua.call('sip:11119916@'+sip_host, options);
    if (session) {
        session.connection.addEventListener('addstream', (e) => {
            var audio = document.getElementById('audio_remote')
            audio.srcObject = e.stream;
            audio.play();  
        });
    }        
}

function hangupCall(){
    ua.terminateSessions();
}
var eventHandlers = {
	'progress': function(e) {
        // $("#ring_timer").countimer('start')
		console.log('call is in progress',e);
	},
	'failed': function(e) {
		console.log('call failed with cause: ', e);
        // $('#btnDialHangup').click();
	},
	'ended': function(e) {
		console.log('call ended with cause: ', e);
        // $('#btnDialHangup').click();
	},
	'confirmed': function(e) {
        
		console.log('call confirmed: ',e);
        console.log("diallogs.....",session._dialog._remote_target._host)
        fs_ip = session._dialog._remote_target._host
        
	}
};



