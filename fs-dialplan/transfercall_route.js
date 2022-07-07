var redis = require('redis');
var redisClient = redis.createClient({host : process.env.REDIS_URL, port : process.env.REDIS_PORT});
'use strict';
module.exports = {
	transfercall_route: function(data,callback) {
		redisClient.exists('transfer_agents',function(err,reply) {
			if(!err) {
		  		if(reply === 1) {
		   			redisClient.get('transfer_agents', function (error, result) {
			   			if (error) {
				    		console.log(error);
				    		throw error;
				    	}else{
				    		var r_data = JSON.parse(result)
				    		r_data[data['transfer_from_agent_uuid']] = data['transfer_to_agent_number']
				    		var agents = JSON.stringify(r_data)
				    		redisClient.set('transfer_agents', agents, function (error, result) {
					    		if (error) {
					        		console.log(error);
					        		throw error;
					    		}else{
									callback(err=null,data);
			    				}
							});
				    	}
					})
		 		} else {
		 				var r_data ={}
			    		r_data[data['transfer_from_agent_uuid']] = data['transfer_to_agent_number']
						var agents = JSON.stringify(r_data)
			    		redisClient.set('transfer_agents', agents, function (error, result) {
				    		if (error) {
				        		console.log(error);
				        		throw error;
				    		}else{
								callback(err=null,data);
		    				}
						});
		  			}
		 	}
		});
	},
	transfercall_del_alert: function(data,callback) {
		redisClient.exists('transfer_agents',function(err,reply) {
			if(!err) {
		  		if(reply === 1) {
		   			redisClient.get('transfer_agents', function (error, result) {
			   			if (error) {
				    		console.log(error);
				    		throw error;
				    	}else{
				    		var r_data = JSON.parse(result)
				    		delete r_data[data['transfer_from_agent_uuid']]
				    		var agents = JSON.stringify(r_data)
				    		redisClient.set('transfer_agents', agents, function (error, result) {
					    		if (error) {
					        		console.log(error);
					        		throw error;
					    		}else{
									callback(err=null,data);
			    				}
							});
				    	}
					})
		 		}
		 	}
		});
	},
}
