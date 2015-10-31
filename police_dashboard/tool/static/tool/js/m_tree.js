function drawChart(text_data,div_id,word){
	var data = google.visualization.arrayToDataTable(text_data);

    var options = {
      wordtree: {
        format: 'implicit',
        word: word
      },
      'tooltip' : {
      			trigger: 'none'
				},
    };

    var chart = new google.visualization.WordTree(document.getElementById(div_id));

    if(div_id==="wordtree_twitter"){
    	// console.log("tab")
    	var container = document.getElementById('menu1');
		google.visualization.events.addListener(chart, 'ready', function () {
			// container.className = container.className.replace( /(?:^|\s)active(?!\S)/g , '' );
			// console.log(container)
		});
    }

    chart.draw(data, options);
	
	function removeGoogleTooltip() {
              var tr = $('g');
              try {
                  $(tr[tr.length-5]).hide();
              }
              catch(e) {
              }
            }

	var tooltip = "<div class='policeTooltip' style='font-size:12px;background:rgba(0,0,0,0.9);padding:12px;border-radius:2px;color:#fff;position:absolute;z-index:10;visibility:hidden'></div>";
	  $(tooltip).appendTo('body');
	  tooltip = $('.policeTooltip');
	  $('#'+div_id).on('mouseover', 'text', function(e){
		  removeGoogleTooltip();              
	      $(tooltip).css('visibility', 'visible')
	  }).on('mousemove', 'text', function(e){
		  removeGoogleTooltip();
	      $(tooltip).css('left', e.pageX+10  +'px').css('top', e.pageY+10 + 'px').html('Click to analyze <strong><span style="color:#EF4C48">"'+ $(this).html() + '"</span></strong><br/> branch')
	  }).click(function(){$(tooltip).css('visibility','hidden')
	  }).on('mouseout', 'text', function(){$(tooltip).css('visibility','hidden')
	  }); 
    
}