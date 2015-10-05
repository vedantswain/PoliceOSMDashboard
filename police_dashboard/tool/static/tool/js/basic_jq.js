$(document).ready(function() {

        // JQuery code to be added in here.
        $('.compare-to').click(function(){
		    // var catid;
		    handle = $(this).html();
		     $.get('/main/load_name/',{handle_name:handle}, function(data){
		               $('#compare-to-1').html(data);
		               // $('#likes').hide();
		           });
		});

});