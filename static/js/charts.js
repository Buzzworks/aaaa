// Note:Live Graph chart is in admin_vue js page 
$('.highcharts-credits').addClass('d-none')
// setInterval(function(){
//     TotalDataFunction()
//     CampCallPerHour()
//     AgentCallsPerHour()
//     }, 60*60*1000
// );

piechart_option = {
    chart: {
        renderTo:'TD_piechart',
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie',
    },
    title: {
        text: ''
    },
    credits: {
     text: 'Flexydial 4.0',
     href: '#'
  },
    // tooltip: {
    //     pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>' // for percentage enable
    // },
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
                enabled: true,
                // format: '<b>{point.name}</b>: {point.percentage:.1f} %' //for percentage format
            },
            showInLegend: true
        }
    },
    series: [{
      name:'Total Count',
      data:[] //Data is updated in the TotalDataFunction() 
    }]
};

//Bar Chart -- High Chart  
barchart_options = {
    chart: {
        renderTo:'agent_HR_barChart',
        type: 'column',
    },
       credits: {
        text: 'Flexydial 4.0',
        href: '#'
     },
      title: {
            text: 'Agent Wise Calls'
      },
      xAxis: {
        type: 'category',
    },
     yAxis: {
        allowDecimals: false,
        min: 0,
        title: {
            text: 'Agent wise Calls'
        }
    },
     legend: {
        enabled: false
    },
    series:[{
      name:'Call Count',
   }] //Data is updated in the AgentCallsPerHour() 
}; 


//Live Calls Data Chart -- High Chart  
testchart_options = {
    chart: {
      renderTo:'camp_HR_linechart',
        type: 'spline',
        animation: false
    },
       credits: {
        text: 'Flexydial 4.0',
        href: '#'
     },
       title: {
            text: 'Campaign Calls'
      },
    xAxis: {
        categories: ["9:00 Am", "10:00 Am", "11:00 Am", "12:00 Pm", "1:00 Pm", "2:00 Pm",
          "3:00 Pm", "4:00 Pm", "5:00 Pm", "6:00 Pm", "7:00 Pm", "8:00 Pm", "9:00 Pm"],
    },
    yAxis: {
      allowDecimals: false,
        title: {
            text: 'Call Count',
        }
    },
    series:[] //live data from the CampCallPerHour()
};        

function TotalDataFunction(){
  if(piechart_live !== undefined){
    piechart_live.destroy()
    } 
    piechart_live = new Highcharts.Chart(piechart_option);
    $.ajax({
    type:'get',
    header: {"X-CSRFToken": csrf_token},
    url: '/api/get-piechartlivedata/',
    success: function(data) {
     piechart_live.series[0].setData([]);
     piechart_live.series[0].addPoint({name:'Dialed',y:data['dialed_count'],color:'#04B76B'})
     piechart_live.series[0].addPoint({name:'NotDialed',y:data['notdialed_count'],color:'#392C70'})
     piechart_live.series[0].addPoint({name:'Queued',y:data['queuecall_count'],color:'#000000'})
     piechart_live.series[0].addPoint({name:'Drop',y:data['dropcall_count'],color: '#FF5E6D'})
     piechart_live.series[0].addPoint({name:'AbandonedCall',y:data['abandoned_count'],color:'#FF6347'})
     piechart_live.series[0].addPoint({name:'CallBack',y:data['callback_count'],color:'#5E50F9'})
     piechart_live.series[0].addPoint({name:'DNC',y:data['dnc_count'],color:'#696969'})
     piechart_live.series[0].addPoint({name:'NC',y:data['nc_count'],color:"#cce2ef"})
     piechart_live.series[0].addPoint({name:'Invalid Number', y:data['InvalidNumber_count'],color:"#6099be"})
     piechart_live.series[0].addPoint({name:'CBR', y:data['cbr_count'],color:"#F5A623"})
    }
  });
}


function AgentCallsPerHour(){
  if(barchart_live !== undefined){
    barchart_live.destroy() 
  } 
  barchart_live = new Highcharts.Chart(barchart_options);
  $.ajax({
    type:'get',
    header: {"X-CSRFToken": csrf_token},
    url: '/api/get-barchartlivedata/',
    success: function(data) {
      barchart_live.series[0].setData(data)
    }
  });
}

function CampCallPerHour(){
  if(linechart_high !== undefined){
    linechart_high.destroy() 
  } 
  linechart_high = new Highcharts.Chart(testchart_options);
  $.ajax({
    type:'get',
    header: {"X-CSRFToken": csrf_token},
    url: '/api/get-multilinechartdata/',
    success: function(data) {
      $.each(data, function(k,v){  
        linechart_high.addSeries({name:v['label'],data:v['data']})
      })
    }
  });
}
