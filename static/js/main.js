'use strict';

$(document).ready(function(){
	// console.log("Test coin_data print:")
	// console.log(coin_data2)

	// var	raw_data = {
	// 		'price': [7436.57, 7572.7, 7972.7, 7272.71, 7172.7, 7265.0, 7460.0, 6691.83], 
	// 		'trans_time': ['2018-03-22T14:59:27.077604', '2018-03-23T16:19:16.457902', '2018-03-24T16:19:26.503031', '2018-03-29T16:12:35.629449', '2018-03-29T16:19:45.504431', '2018-03-29T16:23:55.414867', '2018-03-30T16:20:06.884502', '2018-03-30T14:03:58.681128']
	// 	}
	var	dict_data_manual = [
			{'price': 7436.57, 'trans_time': '2018-03-22T14:59:27.077604'}, 
			{'price': 7572.7, 'trans_time': '2018-03-23T16:19:16.457902'},
			{'price': 7972.7, 'trans_time': '2018-03-24T16:19:26.503031'},
			{'price': 7172.71, 'trans_time': '2018-03-29T12:19:35.629449'},
			{'price': 7265.0, 'trans_time': '2018-03-29T16:19:55.414867'},
			{'price': 7460.0, 'trans_time': '2018-03-29T23:20:06.884502'},
			{'price': 6691.83, 'trans_time': '2018-03-30T14:03:58.681128'},
		]
	// console.log(dict_data_manual)
	


	function getData() {
		var result;
		$.ajax({
			type: "GET",
			url: "/graph/get_data",
			success: function(data){
				console.log("Success function:", data);
				createGraph(data);
				return data;
				},
			error: function(){
				console.log("****Date Records Load Error****");
				}
		}); //end ajax	
	};

	console.log("Start:")
	getData();
	console.log(":End")

	function createGraph(dict_data) {

		var	margin = {top: 60, right: 40, bottom: 30, left: 45},
			height = 400 - margin.top - margin.bottom,
			width = 600 - margin.left - margin.right;
			
		var parseTime = d3.timeFormat("%x %X");
			
		for (var i = 0; i < dict_data.length; ++i) {
			dict_data[i].price = +dict_data[i].price
			dict_data[i].trans_time = new Date(dict_data[i].trans_time)
		}
		// console.log("Last step:", dict_data)
			
		
		var xScale = d3.scaleTime()
			.domain([d3.min(dict_data, function(d) {
						return d.trans_time; }),
					d3.max(dict_data, function(d) {
						return d.trans_time; })
					])
			.range([0, width])

		var yScale = d3.scaleLinear()
			.domain([d3.min(dict_data, function(d) {
						return d.price; }),
					d3.max(dict_data, function(d) {
						return d.price;
					})])
			.range([height, 0])
		
		var xAxis = d3.axisBottom(xScale)

		var yAxis = d3.axisLeft(yScale)
			.ticks(5)

		var line = d3.line()
			.x(function(d) {return xScale(d.trans_time)})
			.y(function(d) {return yScale(d.price)})


		var tooltip = d3.select('body')
			.append('div')
			.style('background', 'white')
			.style('position', 'absolute')
			.style('opacity', 0)

		// Create SVG
		var svg = d3.select(".linechart")
			.append('svg')
				.attr('width', width + margin.left + margin.right)
				.attr('height', height + margin.top + margin.bottom)
				.style('background', '#C9D7D6')

		// Adds circles of every data point
		var scatter = svg.append('g')
				.selectAll('dot')
				.data(dict_data)
				.enter()
			.append('circle')
				.attr('r', 3)
				.attr('cx', function(d) { return xScale(d.trans_time) })
				.attr('cy', function(d) { return yScale(d.price) })
				.attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')
			.on('mouseover', function(d, i) {
				tooltip.transition()
					.duration(200)
					.style('opacity', .9)
				tooltip.html(
					'<div>' + d.price + '<br>' + parseTime(d.trans_time) + '</div>'
					)
					.style('left', (d3.event.pageX - 35) + 'px')
					.style('top', (d3.event.pageY - 35) + 'px')
				d3.select(this)
				.style('opacity', .5)
			})
			.on('mouseout', function(d) {
				d3.select(this)
				.style('opacity', 1)
			});


		// Add line chart
		var path = svg.append('path')
			.attr('fill', 'none')
			.attr('stroke', 'steelblue')
			.attr('stroke-linejoin', 'round')
			.attr('stroke-linecap', 'round')
			.attr('stroke-width', 1.5)
			.attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')
			.attr('d', line(dict_data));

		// Add the y-axis
		var yGuide = svg.append('g')
			.attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')
			.call(yAxis)
		
		// Add the x-axis
		var xGuide = svg.append('g')
			.attr('transform', 'translate(' + margin.left + ',' + (height+margin.top) + ')')
			.call(xAxis)
	} //end createGraph

}); //end doc