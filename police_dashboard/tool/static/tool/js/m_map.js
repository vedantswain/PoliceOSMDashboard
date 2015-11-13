document.getElementById("refresh-btn").addEventListener("click", function(){
    refreshIndexPage();

    $('html,body').animate({
        scrollTop: 0},
        'slow');
});

function refreshIndexPage(){
    var police_blocks = document.getElementsByClassName("col-md-4 col-sm-6 hero-feature");
    
    for(var i = 0; i < police_blocks.length; i++)
    {
       var block=police_blocks.item(i);
        block.style.display = 'block';
    }
}

function updateIndexPage(state) {
    var police_blocks = document.getElementsByClassName("col-md-4 col-sm-6 hero-feature");
    
    for(var i = 0; i < police_blocks.length; i++)
    {
       var block=police_blocks.item(i);
        var block_state=block.getAttribute("data-state");
        // console.log(state);
        if (state===block_state){
            block.style.display = 'block';
        }
        else if (state==="Andhra Pradesh" && block_state==="Telangana"){
            block.style.display = 'block';
        }
        else {
            // console.log(block_state);
            block.style.display = 'none';
        }
    }

    $('html,body').animate({
        scrollTop: $("#home").offset().top},
        'slow');
	// console.log(state);
}


google.setOnLoadCallback(drawRegionsMap);
  dataArray = [['State'],
      ['Andaman and Nicobar Islands'],
        ['Andhra Pradesh'],
        ['Arunachal Pradesh'],
        ['Assam'],
        ['Bihar'],
        ['Chandigarh'],
        ['Chhattisgarh'],
        ['Dadra and Nagar Haveli'],
        ['Daman and Diu'],
        ['Delhi'],
        ['Goa'],
        ['Gujarat'],
        ['Haryana'],
        ['Himachal Pradesh'],
        ['Jammu and Kashmir'],
        ['Jharkhand'],
        ['Karnataka'],
        ['Kerala'],
        ['Lakshadweep'],
        ['Madhya Pradesh'],
        ['Maharashtra'],
        ['Manipur'],
        ['Meghalaya'],
        ['Mizoram'],
        ['Nagaland'],
        ['Orissa'],
        ['Puducherry'],
        ['Punjab'],
        ['Rajasthan'],
        ['Sikkim'],
        ['Tamil Nadu'],
        ['Telangana'],
        ['Tripura'],
        ['Uttar Pradesh'],
        ['Uttarakhand'],
        ['West Bengal']
              ];
  function drawRegionsMap() {
    var data = google.visualization.arrayToDataTable(dataArray);

    var options = {
        region: 'IN',
    	displayMode: 'regions',
        resolution: 'provinces',
        defaultColor: '#145571',
        domain: 'IN',
        backgroundColor: '#eee',
        enableRegionInteractivity: true
   	};

      function clickHandler() {
                  var selection = chart.getSelection();
    var state = '';
    for (var i = 0; i < selection.length; i++) {
        var item = selection[i];
		var stateIndex = item.row;
        if(stateIndex != null) {
        	state = dataArray[stateIndex + 1][0];
            updateIndexPage(state);
        }
        
      }
   }
      
    var chart = new google.visualization.GeoChart(document.getElementById('regions_div'));
    google.visualization.events.addListener(chart, 'select', clickHandler);
      
      
    chart.draw(data, options);
}