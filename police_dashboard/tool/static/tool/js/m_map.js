document.getElementById("refresh-btn").addEventListener("click", function(){
    refreshIndexPage();
    $('#no-block-msg').hide();
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
    var hidden_count = 0
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
            hidden_count+=1;
        }
    }

    if (hidden_count == police_blocks.length){
        // console.log("equal");
        $('#no-block-msg').show();
    }
    else{
        // console.log("unequal");
        $('#no-block-msg').hide();
    }
    $('html,body').animate({
        scrollTop: $("#home").offset().top},
        'slow');
	// console.log(state);
}

function makeMap(dataArr){
  google.setOnLoadCallback(drawRegionsMap);
  dataArray = dataArr

  function drawRegionsMap() {
    var data = google.visualization.arrayToDataTable(dataArray);

    var options = {
        region: 'IN',
        displayMode: 'regions',
        resolution: 'provinces',
        defaultColor: '#145571',
        colorAxis: {colors: ['#bbdae7', '#145571']},
        domain: 'IN',
        backgroundColor: '#eee',
        legend: 'none',
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
}