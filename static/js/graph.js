InitChart();

function InitChart() {

  data = data.replace(/&#34;/g, '"')

  //var lineData = JSON.parse('[{"date": 1432128000000, "freq": 1}, {"date": 1432138397000, "freq": 2}, {"date": 1432136412000, "freq": 1}]');
  var lineData = JSON.parse(data);
  //for (var i=0; i<lineData.length; i++ ){
  //  lineData[i].date=new Date(lineData[i].date);
  //  console.log(lineData[i].date);
  //}

  var yMax = 0; //keep track of highest value

  //loop through array of objects
  for (var i=0, len = lineData.length; i<len; i++) {
    var value = Number(lineData[i]["freq"]);
    if (value > yMax) {
        yMax = value;
    }
  }
  console.log(lineData);
  if (yMax==0){  
      document.getElementById("noResultsMsg").innerHTML = "No results found"; 
    }
    else {
        var div = d3.select("body").append("div")   
        .attr("class", "tooltip")               
        .style("opacity", 0);

        var vis = d3.select("#graph"),
        WIDTH = 800, 
        HEIGHT = 500,
        MARGINS = {
          top: 20,
          right: 20,
          bottom: 150,
          left: 50
        },
        xRange = d3.scale.linear().range([MARGINS.left, WIDTH - MARGINS.right]).domain([d3.min(lineData, function (d) {
            return d.date;
          }),
          d3.max(lineData, function (d) {
            return d.date;
          })
        ]),

        yRange = d3.scale.linear().range([HEIGHT - MARGINS.top, MARGINS.bottom]).domain([d3.min(lineData, function (d) {
            return d.freq;
          }),
          d3.max(lineData, function (d) {
            return d.freq;
          })
        ]),

        xAxis = d3.svg.axis()
          .scale(xRange)
          //.tickSize(5)
          .tickFormat(function(d) { return d3.time.format('%b %d %m %H:%M:%S')(new Date(d)); })
          .tickSubdivide(true),

        yAxis = d3.svg.axis()
          .scale(yRange)
          .ticks(yMax)
          .tickSize(5)
          .orient("left")
          .tickSubdivide(false);

      vis.append("svg:g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + (HEIGHT - MARGINS.bottom) + ")")
        .call(xAxis)
        .selectAll("text")  
                .style("text-anchor", "end")
                .attr("dx", "-.8em")
                .attr("dy", ".15em")
                .attr("transform", function(d) {
                    return "rotate(-65)" 
                    });

      vis.append("svg:g")
        .attr("class", "y axis")
        .attr("transform", "translate(" + (MARGINS.left) + "," + (- MARGINS.bottom+20) +")")
        .call(yAxis);

      var lineFunc = d3.svg.line()
      .x(function (d) {
        return xRange(d.date);
      })
      .y(function (d) {
        return yRange(d.freq);
      })
      .interpolate('linear');

    vis.append("svg:path")
      .attr("d", lineFunc(lineData))
      .attr("stroke", "blue")
      .attr("stroke-width", 2)
      .attr("fill", "none")
      .attr("transform", "translate(0," + (- MARGINS.bottom+20) +")");

    vis.selectAll("dot")    
            .data(lineData)         
        .enter().append("svg:circle")                               
            .attr("r", function(d) { if (d.freq>0) return 5; })       
            .attr("cx", function(d) { if (d.freq>0) return xRange(d.date); })       
            .attr("cy", function(d) { if (d.freq>0) return yRange(d.freq)-130; })     
            .on("mouseover", function(d) {      
                div.transition()        
                    .duration(200)      
                    .style("opacity", .9);      
                div .html(d3.time.format('%b %d %m %H:%M:%S')(new Date(d.date)) + "<br/>"  + d.freq)  
                    .style("left", (d3.event.pageX) + "px")     
                    .style("top", (d3.event.pageY - 28) + "px");    
                })                  
            .on("mouseout", function(d) {       
                div.transition()        
                    .duration(500)      
                    .style("opacity", 0);   
            });
          }
}
