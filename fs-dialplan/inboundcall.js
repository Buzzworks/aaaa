var fs = require('fs');
var https = require('https');
esl = require('esl')
var ca = fs.readFileSync('wss.pem');
var redis = require('redis');
var redisClient = redis.createClient({host : process.env.REDIS_URL, port : process.env.REDIS_PORT});
var options = {
  host: process.env.HOST_URL
, port: 443
, path: '/inbound_agents/'
, ca: ca
, rejectUnauthorized:false
, method:'POST',
};

redisClient.on('ready',function() {
 		console.log("Redis is ready");
});

redisClient.on('error',function() {
 console.log("Error in Redis");
});

module.exports = {
	availale_agents: function(req,caller_id,dialed_uuid,server,destination_number,intiate_time,callback) {
		var body = JSON.stringify({"caller_id":caller_id,"dialed_uuid":dialed_uuid,"server":server,"destination_number":destination_number,"intiate_time":intiate_time});
		options.path = '/rec_inbound_agents/'
		options.headers ={
	 		'Content-Length': Buffer.byteLength(body),
	    	'Content-Type': 'application/x-www-form-urlencoded'
		}
		options.agent = new https.Agent(options);
		django_req = https.request(options, function(res, body) {
			res.on('data', function (data) {
				try{

					data = JSON.parse(data)
					data['destination_number']= destination_number
					data['dialed_uuid']= dialed_uuid
					if (data['cust_status']=='true'){
						var rec_fun = setTimeout(function(){module.exports.availale_agents(req,caller_id,dialed_uuid,server,destination_number,intiate_time,function(err,data){
							callback(err=null,data)
						})},10000)
						   redisClient.get('inbound_agents', function (error, result) {
							   if (error) {
								console.log(error);
								throw error;
							}else{
								var r_data = JSON.parse(result)
								r_data[dialed_uuid] = data['extension']
								var agents = JSON.stringify(r_data)
								redisClient.set('inbound_agents', agents, function (error, result) {
									if (error) {
										console.log(error);
										throw error;
									}
								});
							}
						})
					}else{
						  clearTimeout(rec_fun);
						  // callback(err=null,data)
					}
					callback(err=null,data)
				}catch(e){
					util.log(e)
					django_req.write(body)
					django_req.end()
					return
				}
			})
		})
		django_req.write(body)
		django_req.end()
		django_req.on('uncaughtException', function (err) {
			util.log("****************")
			util.log(err);
		});
		django_req.on('error',(err)=>{
			util.log("---------------")
			util.log(err)
		})
	},
	inboundcall_route: function(req,caller_id,dialed_uuid,server,destination_number,callback) {
		var body = JSON.stringify({"caller_id":caller_id,"dialed_uuid":dialed_uuid,"server":server,"destination_number":destination_number});
		options.path = '/inbound_agents/'
		options.headers ={
			'Content-Length': Buffer.byteLength(body),
			'Content-Type': 'application/x-www-form-urlencoded'
		}
		options.agent = new https.Agent(options);
		django_req = https.request(options, function(res, body) {
			res.on('data', function (data) {
				try{
					data = JSON.parse(data)
					// if(data['wfh']==true){
					// 	callback(err=null,data);
					// }else{
					redisClient.exists('inbound_agents',function(err,reply) {
						if(!err) {
							if('dial_method' in data | 'queue_call' in data | 'skill_routed_status' in data){
								if(data['dial_method']['ibc_popup']==true | data['queue_call']==false){
										if(reply === 1) {
											redisClient.get('inbound_agents', function (error, result) {
												if (error) {
												console.log(error);
												throw error;
											}else{
												var r_data = JSON.parse(result)
												r_data[dialed_uuid] = data['extension']
												var agents = JSON.stringify(r_data)
												redisClient.set('inbound_agents', agents, function (error, result) {
													if (error) {
														console.log(error);
														throw error;
													}else{
														callback(err=null,data);
													}
												});
											}
										})
										}else {
											var r_data = {}
											r_data[dialed_uuid] = data['extension']
											var agents = JSON.stringify(r_data)
											redisClient.set('inbound_agents', agents, function (error, result) {
												if (error) {
													console.log(error);
													throw error;
												}else{
													callback(err=null,data);
												}
											});
										}
									}else{
										callback(err=null,data);
									}
							}
							}
					});
				}catch(e){
					util.log(e)
					django_req.write(body)
					django_req.end()
					return
				}
				// }
			});
		});
		django_req.write(body)
		django_req.end()
		django_req.on('uncaughtException', function (err) {
			util.log("****************")
			util.log(err);
		});
		django_req.on('error',(err)=>{
			util.log("---------------")
			util.log(err)
		})
	},

	inboundcall_dis_alert: function(answered_agent,dialed_uuid,state,callback) {
		redisClient.get('inbound_agents', function (error, result) {
			try{
				if (error) {
					console.log(error);
					throw error;
				}
				var data = JSON.parse(result)
				var list_data = data[dialed_uuid]
				if(state=='answer'){
					var agents = list_data.splice(list_data.indexOf(answered_agent),1);
					callback(err=null,list_data);
				}else if(state=='hangup'){
					callback(err=null,list_data);
				}
			}catch(e){
				util.log(e)
				django_req.write(body)
				django_req.end()
				return
			}
		    
		});
	},

	inboundcall_del_alert: function(dialed_uuid) {
		redisClient.get('inbound_agents', function (error, result) {
			try{
				if (error) {
					console.log(error);
					throw error;
				}
				var data = JSON.parse(result)
				delete data[dialed_uuid]
				var agents = JSON.stringify(data)
				redisClient.set('inbound_agents', agents, function (error, result) {
					if (error) {
						console.log(error);
						throw error;
					}
				});
			}catch(e){
				util.log(e)
				django_req.write(body)
				django_req.end()
				return
			}
		    
			});
	},

	wfh_client_hangup: function(dialed_uuid,action) {
		try{
			client = esl.createClient()
			client.on ('esl_auth_request',function(call) {
				call.auth ('ClueCon',function(){
					if(action == 'hangup'){
						cmd = `uuid_kill ${dialed_uuid}`
					}else if(action == 'customer_name'){
						cmd = `uuid_audio ${uuid} start write mute -4`
					}else if(action == 'customer_number'){
						cmd = `uuid_audio ${uuid} start write mute -4`
					}else if(action == 'mute'){
						cmd = `uuid_audio ${uuid} start write mute -4`
					}else if(action == 'unmute'){
						cmd = `uuid_audio ${uuid} start write mute 0`
					}
					call.api(cmd);
				});
			});client.connect(8021, '0.0.0.0')
		}catch(e){
			util.log(e)
			django_req.write(body)
			django_req.end()
			return
		}
	},

	wfh_customer_details_route: function(req,uuid,session_uuid,action,callback) {
		try{
			var w_body = JSON.stringify({"uuid":uuid,'session_uuid':session_uuid,'action':action});
			options.path = '/wfh_customer_details/'
			options.headers ={
				 'Content-Length': Buffer.byteLength(w_body),
				'Content-Type': 'application/x-www-form-urlencoded'
			}
			options.agent = new https.Agent(options);
			w_django_req = https.request(options, function(res, w_body) {
				res.on('data', function (data) {
					data = JSON.parse(data)
					callback(err=null,data);
			  });
			});
		}catch(e){
			util.log(e)
			django_req.write(body)
			django_req.end()
			return
		}

		w_django_req.write(w_body)
		w_django_req.end()
		w_django_req.on('uncaughtException', function (err) {
			util.log("****************")
			util.log(err);
		});
		w_django_req.on('error',(err)=>{
			util.log("---------------")
			util.log(err)
		})
	},
}
