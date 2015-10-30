$(document).ready(function() {
        // JQuery code to be added in here.
        $(".help-popover").popover();

        $('#menu1').addClass('active')

        $('.compare-to-graph1-twitter').click(function(){
		    // var catid;
		    pf="twitter"
		    handle = $('#twitter-handle-name').html()
		    comp_handle = $(this).find(".comp-fb-handle").text();
		    $('#graph1-tw-loader').show();
		    $.get('/main/graph_comp/',{handle_name:handle,comp_handle_name:comp_handle,platform:pf}, function(data){
		               $('#graph1-twitter').html(data);
		               // $('#likes').hide();
		               $('#graph1-tw-loader').hide();
		           });
		    return false;
		});

		$('.compare-to-graph1-facebook').click(function(){
		    // var catid;
		    pf="facebook"
		    handle = $('#facebook-handle-name').html()
		    comp_handle = $(this).find(".comp-fb-handle").text();
		    $('#graph1-fb-loader').show();
		    $.get('/main/graph_comp/',{handle_name:handle,comp_handle_name:comp_handle,platform:pf}, function(data){
		               $('#graph1-facebook').html(data);
		               // $('#likes').hide();
		               $('#graph1-fb-loader').hide();
		           });
		    return false;
		});

        $('.victimzn-key-twitter').click(function(){
		    // var catid;
		    pf="twitter"
		    handle = $('#twitter-handle-name').html()
			var old_key = $('#victimzn-curr-key-twitter').html()
			// console.log(old_key)
		    var key = $(this).html();
		    var mObj = $(this)
		    $('#graph2-tw-loader').show();
		    $.get('/main/victimisation_tree/',{handle_name:handle,keyword:key,platform:pf}, function(data){
		               $('#graph2-twitter').html(data);
		               // $('#likes').hide();
		               $('#graph2-tw-loader').hide();
		               mObj.html(old_key);
		    		   $('#victimzn-curr-key-twitter').html(key);
		           });
		    return false;
		});

		$('.victimzn-key-facebook').click(function(){
		    // var catid;
		    pf="facebook"
		    handle = $('#facebook-handle-name').html()
			var old_key = $('#victimzn-curr-key-facebook').html()
			// console.log(old_key)
		    var key = $(this).html();
		    var mObj = $(this)
		    $('#graph2-fb-loader').show();
		    $.get('/main/victimisation_tree/',{handle_name:handle,keyword:key,platform:pf}, function(data){
		               $('#graph2-facebook').html(data);
		               // $('#likes').hide();
		               $('#graph2-fb-loader').hide();
		               mObj.html(old_key);
		    		   $('#victimzn-curr-key-facebook').html(key);
		           });
		    return false;
		});

		// $('.victimzn-key-twitter').click(function(){
		//     // var catid;
		//     pf="twitter"
		//     handle = $('#twitter-handle-name').html()
		// 	var old_key = $('#victimzn-curr-key-twitter').html()
		// 	// console.log(old_key)
		//     var key = $(this).html();
		//     var mObj = $(this)
		//     $('#graph2-tw-loader').show();
		//     $.get('/main/victimisation_tree/',{handle_name:handle,keyword:key,platform:pf}, function(data){
		//                $('#graph2-twitter').html(data);
		//                // $('#likes').hide();
		//                $('#graph2-tw-loader').hide();
		//                mObj.html(old_key);
		//     		   $('#victimzn-curr-key-twitter').html(key);
		//            });
		//     return false;
		// });
		$('#fb-actual-posts-Modal').on('shown.bs.modal', function() {
		    pf="facebook"
		    handle = $('#facebook-handle-name').html()
			var old_key = $('#victimzn-curr-key-facebook').html()
			var key = old_key
		    $.get('/main/victimisation_actual/',{handle_name:handle,keyword:key,platform:pf}, function(data){
		               $('#actual-posts-modal-body').html(data);
		               // $('#likes').hide();
		               // $('#graph2-fb-loader').hide();
		           });
		    return false;
		})

		$('.cloud-key-wordcloud_facebook').click(function(){
		    // var catid;
		    console.log("clicked")
		    pf="facebook"
		    handle = $('#facebook-handle-name').html()
		    var key = $(this).html();
		    $('#graph3-fb-loader').show();
		    $.get('/main/word_cloud/',{handle_name:handle,keyword:key,platform:pf}, function(data){
		    		   $('#graph3-facebook').html(data.cloud);
		               $('#graph3-fb-loader').hide();
		           });
		    return false;
		});

		$('.cloud-key-wordcloud_twitter').click(function(){
		    // var catid;
		    console.log("clicked")
		    pf="twitter"
		    handle = $('#twitter-handle-name').html()
		    var key = $(this).html();
		    $('#graph3-tw-loader').show();
		    $.get('/main/word_cloud/',{handle_name:handle,keyword:key,platform:pf}, function(data){
		    		   $('#graph3-twitter').html(data.cloud);
		               $('#graph3-tw-loader').hide();
		           });
		    return false;
		});

});