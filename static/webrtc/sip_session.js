function sipInitialize()
{
	var readyCallback = function(e){
		createSipStack(); // see next section
	};
	var errorCallback = function(e)
	{
	console.error('Failed to initialize the engine: ' + e.message);
	}
	SIPml.init(readyCallback, errorCallback);

	console.info("WINDOW ONLOAD");
}
var sipStack=true;
var callSession;
function createSipStack()
{

	var eventsListener = function(e){
		if(e.type == 'started'){
					login();
		}
		else if(e.type == 'i_new_message'){ // incoming new SIP MESSAGE (SMS-like)
			acceptMessage(e);
		}
		else if(e.type == 'failed_to_start'){
				
			}
		else if(e.type == 'i_new_call'){ // incoming audio/video call
			acceptCall(e);
		}
	}
	sipStack = new SIPml.Stack({
						realm: host, // mandatory: domain name
						impi: extension, // mandatory: authorization name (IMS Private Identity)
						impu: sip_identity, // mandatory: valid SIP Uri (IMS Public Identity)
						password: user_pass, // optional
						display_name: user_name, // optional
						websocket_proxy_url: websocket_proxy_url, // optional
						outbound_proxy_url:outbound_proxy_url, // optional
						enable_rtcweb_breaker: false, // optional
						// ice_servers:  [],
						events_listener: { events: '*', listener: eventsListener }, 		
			sip_headers: [ // optional
						{ name: 'User-Agent', value: user_name},
						{ name: 'Organization', value: 'Buzzworks telecom' }
				]
			}
		);
	if((sipStack.start() != 0)){
		SIPml["b_initialized"]=false
		sipInitialize()	
	}
}

var registerSession;
var reg_eventsListener = function(e){
	if(e.type == 'transport_error'){
		SIPml["b_initialized"]=false
		sipInitialize()
	}
	if(e.type == 'connected' && e.session == registerSession){
		makeCall();
	}
}

function login(){
	registerSession = sipStack.newSession('register', {
		events_listener: { events: '*', listener: reg_eventsListener } // optional: '*' means all events
	});
	registerSession.register();
}

var callEventsListener = function(e)
	// call events handled here
	{
		if (e.type == "connecting") {
			$('.preloader').fadeIn('fast')
		}
		else if (e.type == "terminated") {
			if (sip_login == true){
				// sipStack.stop()
				// // sipStack.start()
				// // sip_error = false
				SIPml["b_initialized"]=false
				sipInitialize()
				console.log('terminated event called')
			}else{
				$('.preloader').fadeOut('slow')
			}
		}
		else if (e.type == "m_stream_audio_remote_added") {
			sip_error = false
			$('.preloader').fadeOut('slow')
			}
		else if (e.type == "connected") {
		}
	}

function create_call_session () {
	// This function is used to create call session
	return sipStack.newSession('call-audio', {
		audio_remote: document.getElementById('audio_remote'),
		events_listener: { events: '*', listener: callEventsListener } // optional: '*' means all events
	});
}

function makeCall()
{
	ocallSession = create_call_session()
	if (ocallSession) {
		ocallSession.call('11119916')
	}else{
		errorAlert('OOPS!!! Something Went Wrong',"Error in Call")
	}
}

function send_dtmf(dtmf_value) {
	var dtmf_value = dtmf_value.split("");
	if (dtmf_value){ 
		if (ocallSession) {
			ocallSession.dtmf('*')
			ocallSession.dtmf('1')
			for (var i in dtmf_value) {
				// alert(dtmf_value[i])
				ocallSession.dtmf(dtmf_value[i]);
			}
		}
	}
}

function click_dtmf(dtmf_value) {
	// var dtmf_value = dtmf_value.split("");
	if (dtmf_value){ 
		data = {
			'Unique-ID'  : session_details[extension]['Unique-ID'],
			'dialed_uuid': session_details[extension]['dialed_uuid'],
			'sip_server': session_details[extension]['variable_sip_from_host'],
			'dtmf_digit': dtmf_value
		}
		try { 
			$.ajax({
				type:'post',
				headers:{'X-CSRFToken':csrf_token},
				url: '/api/send_dtmf/',
				data:data,
				success:function(data) {
					if('success' in data){
						agent_beep_file= document.getElementById("autodial_agent_beep");
			            agent_beep_file.play() 
					}	
				}
			})
		} catch (e) { console.log(e)}
	}
}

