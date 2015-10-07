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
		});

});