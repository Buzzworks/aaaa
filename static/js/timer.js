// this js is for timer on html

function timer(timer_id, second, minute, hours){
	function time_format(num){
		return( num <10 ? "0" : "")+num;
	}
	second++;
	if (second == 60){
		minute++;
		second = 0;
		if (minute == 60){
			hours++;
			minute = 0;
		}
	}
	setTimerValue(second, minute, hours)
	$(timer_id).val(time_format(hours)+":"+time_format(minute) +":"+time_format(second));
	
}
function timer_reset(){
	second= 0;
	minute =0;
	hours = 0;
	setTimerValue(0,0,0)
	clearInterval(timer);
}

function setTimerValue(sec=0, min=0, hour=0){
		// This function set the timere value in session storage
		sessionStorage.setItem("sec", sec);
		sessionStorage.setItem("min", min);
		sessionStorage.setItem("hrs", hour);
}

// feedback_timer for feedback submition
// function feedback_timer(id, timer_val){
// 	var timer2 = timer_val;
// 	var interval = setInterval(function() {
// 		var timer = timer2.split(':');
// 		//by parsing integer, I avoid all extra string processing
// 		var minutes = parseInt(timer[0], 10);
// 		var seconds = parseInt(timer[1], 10);
// 		--seconds;
// 		minutes = (seconds < 0) ? --minutes : minutes;
// 		if (minutes < 0) clearInterval(interval);
// 		seconds = (seconds < 0) ? 59 : seconds;
// 		seconds = (seconds < 10) ? '0' + seconds : seconds;
// 		//minutes = (minutes < 10) ?  minutes : minutes;
// 		$('#'+id).html(minutes + ':' + seconds);
// 		timer2 = minutes + ':' + seconds;
// 		}, 1000);
// }