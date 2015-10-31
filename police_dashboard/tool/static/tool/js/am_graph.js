function clearAmchart(){
	console.log("clearing")
	var els = document.getElementsByTagName("a"),
	els_length = els.length;
	for (var i = 0, l = els_length; i < l; i++) {
	    var el = els[i];
	   	if (el.title === 'JavaScript charts') {
	   		console.log(el);
	        el.innerHTML = "";
	        // el.style.display = "none";
	        el.href = "#";
	        console.log(el);
	    }
	}
}

function renderGraph(data,div_id,parent_div_id){
	var s_dict=data[0]
	var graphs=[]

	var colors=["#004875",  "#0479CC",  "#91D9FF", "#A62F00",  "#F2784B",  "#EBBC4E"]
	var dashls=[0,1,3,0,1,3]
	// console.log("inside new renderGraph")
	var count= 0;
	for (var key in s_dict) {
	  if (key !== 'date'){
  		var graph= new Object();
		  graph["lineThickness"]=1;
		  graph["title"]=key;
		  graph["valueField"]=key;
		  graph["lineColor"]=colors[count];
		  graph["color"]=colors[count];
		  graph["dashLength"]=dashls[count];
		  graph["balloonText"]="<span style='font-size:10px;'>"+key+": [[value]]</span>";
		  graphs.push(graph);

		  count++;
	  }
	  
	}

	// console.log(data);
	// console.log(graphs)

	var chart = AmCharts.makeChart( div_id, {
	  "type": "serial",
	  "theme": "light",
	  "marginRight": 30,
	  "path": "http://www.amcharts.com/lib/3/",
	  "legend": {
	    "equalWidths": false,
	    "periodValueText": "total: [[value.sum]]",
	    "position": "top",
	    "valueAlign": "left",
	    "valueWidth": 100
	  },
	  "dataProvider": data,
	  "graphs": graphs,
	  "chartCursor": {},
	  "categoryField": "date",
   	 "categoryAxis": {
	   "startOnAxis": true,
	    "gridAlpha": 0.07,
        "parseDates": true,
        "axisColor": "#DADADA",
        "dashLength": 1,
        "minorGridEnabled": true
    },
    "export": {
        "enabled": true
    },
	} );

	/**
	 * Add events
	 */
	
	chart.addListener( "init", function( event ) {
		// console.log(parent_div_id==="tw")
		if(parent_div_id!==""){
		  $(parent_div_id).on('show.bs.collapse', function () {
	      	// console.log("show");
	      	chart.invalidateSize();
	      });
	  	}
	  	
	  	if(parent_div_id==="tw"){
	  		// console.log("satisfied");
		  	$('a[href=#menu1]').on('shown.bs.tab', function (e) {
		  	  // console.log("visible")
			  chart.invalidateSize();
			})
	  	}

	  
	  /**
	   * Add hidden graphs for each value axis guide
	   */
	  setTimeout( function() {
	    for ( var x = 0; x < event.chart.valueAxes.length; x++ ) {
	      for ( var y = 0; y < event.chart.valueAxes[ x ].guides.length; y++ ) {
	        var guide = event.chart.valueAxes[ x ].guides[ y ];
	        var graph = new AmCharts.AmGraph();
	        graph.balloonText = "";
	        graph.lineColor = guide.lineColor;
	        graph.lineAlpha = 1;
	        graph.title = guide.label;
	        graph.valueField = "dummy";
	        graph.legendValueText = "" + guide.value;
	        graph.legendPeriodValueText = "" + guide.value;
	        graph.relatedGuide = guide;
	        chart.addGraph( graph );
	      }
	    }
	  }, 10 );

	    /**
	   * Set legend events
	   */
	  event.chart.legend.addListener("hideItem", function(event) {
	    if (event.dataItem.relatedGuide !== undefined) {
	      event.dataItem.relatedGuide.lineAlpha = 0;
	      event.dataItem.relatedGuide.originalLabel = event.dataItem.relatedGuide.label;
	      event.dataItem.relatedGuide.label = "";
	      event.chart.validateNow();
	    }
	  });
	  
	  event.chart.legend.addListener("showItem", function(event) {
	    if (event.dataItem.relatedGuide !== undefined) {
	      event.dataItem.relatedGuide.lineAlpha = 0.5;
	      event.dataItem.relatedGuide.label = event.dataItem.relatedGuide.originalLabel;
	      event.chart.validateNow();
	    }
	  });
	} );
	}