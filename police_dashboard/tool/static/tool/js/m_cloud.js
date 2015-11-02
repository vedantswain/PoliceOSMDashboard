function renderCloud(frequency_list,div_id){
    // console.log("rendering");

    var fill = d3.scale.category20();

    d3.layout.cloud().size([800, 300])
            .words(frequency_list)
            .padding(10)
            .rotate(0)
            .text(function(d) { return d.word; })
            .fontSize(function(d) { return d.size; })
            .on("end", draw)
            .start();

    function draw(words) {
        
        // console.log("drawing")
        d3.select(div_id).append("svg")
                .attr("width", 1050)
                .attr("height", 350)
                .attr("class", "wordcloud")
                .append("g")
                // without the transform, words words would get cutoff to the left and top, they would
                // appear outside of the SVG area
                .attr("transform", "translate(520,200)")
                .selectAll("text")
                .data(words)
                .enter().append("text")
                .style("font-size", function(d) { return d.size + "px"; })
                .style("fill", function(d, i) { return fill(i); })
                .attr("text-anchor", "middle")
                .attr("transform", function(d) {
                    return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
                })
                .text(function(d) { return decodeURIComponent(escape(d.word)); })
                .call(make_ajax);

                function make_ajax(d)
                {   
                    
                    // $(this).tooltip();

                    this
                      .on("mouseover", function() {
                        $(this).css("cursor","pointer");
                        // $(tooltip).css('visibility', 'visible')
                        var size = parseInt($(this).css('font-size'));
                        size = (size + 2) + "px";
                        $(this).css({'font-size':size});
                      })
                      .on("mousemove", function(e) {
                        // console.log("mousemove");
                        // $(tooltip).css('left', e.pageX+10  +'px').css('top', e.pageY+10 + 'px').html('Click to focus on <strong><span style="color:#EF4C48">"'+ $(this).html() + '"</span></strong><br/> branch')
                      })
                      .on("mouseout",function(){
                        // console.log("mouseout");
                        // $(tooltip).css('visibility','hidden')
                        var size = parseInt($(this).css('font-size'));
                        size = (size - 2) + "px";
                        $(this).css({'font-size':size});
                      })
                      .on("click", function(d) {
                        console.log($(this).html());
                        ajaxCloud($(this).html());
                    });

                  function ajaxCloud(word){
                        console.log("clicked word")
                        if(div_id=="#wordcloud_facebook"){
                            pf="facebook";
                            handle=$('#facebook-handle-name').html();
                            loader='#graph3-fb-loader';
                            graph_div='#graph3-facebook';
                            stub='<div id="wordcloud_facebook"></div>\n'
                        }
                        else{
                            pf="twitter";
                            handle=$('#twitter-handle-name').html();
                            loader='#graph3-tw-loader';
                            graph_div='#graph3-twitter';
                            stub='<div id="wordcloud_twitter"></div>\n'
                        }
                        key=word
                        $(loader).show();
                        $.get('/main/word_cloud/',{handle_name:handle,keyword:key,platform:pf}, function(data){
                                   $(graph_div).html(stub+data.cloud);
                                   $(loader).hide();
                               });
                        return false;
                    }
                }
    }
}