function plotSentiment(data) {
	var SentimentData ='0';
	console.log(data)
	// var json_data = JSON.stringify(eval("(" + data + ")"));
	// console.log(json_data)
	if (data) {
		var donut = Morris.Donut({
			element: 'sentiment-container',
			data: data,
			colors: ['#0072bc','#707f9b', '#455064', '#242d3c','#b92527', '#d13c3e', '#ff6264', '#ffaaab']
		});
		donut.on('click', function(iterator, row) {

    		$('#sentiment-Modal').on('shown.bs.modal', function() {
			    pf="facebook"
			    handle = $('#facebook-handle-name').html()
				var sentiment_label = row.label
				// var key = old_key
			    $.get('/main/sentiment_ajax/',{handle_name:handle,sentiment:sentiment_label,platform:pf}, function(data){
			               $('#sentiment-modal-body').html(data);
			           });
			    return false;
			}).modal('show');
		});


		// donut.el.append("<div class='donut-tooltip'></div>");
	 //    var tooltip = $('div.donut-tooltip').css("background", "rgba(0,0,0,0.9)")
	 //    .css("position", "relative")
	 //    .css("display", "inline")
		// .css("padding", "12px")
		// .css("border-radius", "2px")
	 //    .css("color", "#fff")
	 //    .css("z-index", "10")
	 //    .css("visibility", "hidden")
	 //    .html(function() {
		// 	return "<strong>Frequency:</strong> <span style='color:red'></span>";
		// });

		// $('#sentiment-container svg path').on('mouseover', function() {
		// 	var rowLabel = $('#sentiment-container svg text').first().text().toLowerCase();
		// 	if (rowLabel !== 'neutral') {
		// 		tooltip.css("visibility", "visible").html(function() {
		// 			return "<strong>Click to see posts containing "+rowLabel+" sentiments</strong>";
	 //  			});
		// 	}
		// })
		// .on('mousemove', function(e) {
		// 	var containerPos = $(window).scrollTop() - $('#sentiment-container').offset().top - $('#sentiment-container').height();
		// 	tooltip.css("top",(e.clientY+containerPos)+"px").css("left",(e.clientX-40)+"px")
		// })
		// .on('mouseout', function(iterator, row) {
		// 	tooltip.css("visibility", "hidden");
		// });


	} else $('#sentiment-container').html('<h3><div class="label label-info">Data for this analysis will load in a while.</div></h3>');
}