$(document).ready(function() {

        // JQuery code to be added in here.
        $('.compare-to-graph1-twitter').click(function(){
		    // var catid;
		    handle = $('#twitter-handle-name').html()
		    comp_handle = $(this).html();
		    $('#graph1-tw-loader').show();
		    $.get('/main/graph1_twitter_comp/',{handle_name:handle,comp_handle_name:comp_handle}, function(data){
		               $('#graph1-twitter').html(data);
		               // $('#likes').hide();
		               $('#graph1-tw-loader').hide();
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

});