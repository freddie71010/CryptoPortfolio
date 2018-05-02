'use strict';

$(document).ready(function(){

	var data = [30, 86, 168, 281, 303, 365],
		raw_data = {
			'price': [7436.57, 7572.7, 7972.7, 7272.71, 7172.7, 7265.0, 7460.0, 6691.83], 
			'trans_time': ['2018-03-29T14:59:27.077604', '2018-03-29T16:19:16.457902', '2018-03-29T16:19:26.503031', '2018-03-29T16:19:35.629449', '2018-03-29T16:19:45.504431', '2018-03-29T16:19:55.414867', '2018-03-29T16:20:06.884502', '2018-03-30T14:03:58.681128']
		},
		margin = {top: 0, right: 0, bottom: 30, left: 45},
		height = 400 - margin.top - margin.bottom,
		width = 600 - margin.left - margin.right,
		prices = [],
		trans_times = [];
		
	for (var i = 0; i < raw_data.price.length; ++i) {
		prices.push(raw_data.price[i])
		trans_times.push(new Date(raw_data.trans_time[i]))
	}
	console.log(prices)
	console.log(trans_times)
		

	var myChart,
		xScale,
		xAxisValues,
		xAxisTicks,
		xGuide,
		yScale,
		yAxisValues,
		yAxisTicks,
		yGuide,
		timeParse,
		tooltip;

	timeParse = d3.timeParse("%d-%b-%y");

	// set scales
	xScale = d3.scaleBand()
		.domain(prices)
		.paddingInner(.1)
		.paddingOuter(.1)
		.range([0, width]);

	yScale = d3.scaleLinear()
		.domain([0, d3.max(prices)])		// Data values to use in scale
		.range([0, height]);			// Range that the values will scale to fit in

	xAxisValues = d3.scaleTime()
		.domain([trans_times[0], trans_times[(trans_times.length - 1)]])
		.range([0, width])

	yAxisValues = d3.scaleLinear()
		.domain([0, d3.max(prices)])
		.range([height, 0])

	xAxisTicks = d3.axisBottom(xAxisValues)
		.ticks(d3.timeDay.every(.25))

	yAxisTicks = d3.axisLeft(yAxisValues)
		.ticks(10)


	tooltip = d3.select('body')
		.append('div')
		.style('background', 'white')
		.style('position', 'absolute')
		.style('opacity', 0)

	myChart = d3.select(".barchart")
		.append('svg')
			.attr('width', width + margin.left + margin.right)
			.attr('height', height + margin.top + margin.bottom)
			.style('background', '#C9D7D6')
		.append('g')
			.attr('transform', 'translate(' + (margin.left + margin.right) +',0)')
		.selectAll('rect')
		.data(prices)
		.enter()
		.append('rect')
			.attr('fill', '#C61C6F')
			.attr('width', function(d) {
				return xScale.bandwidth();
			})
			.attr('height', function(d) {
				return yScale(d);
			})
			.attr('x', function(d) {
				return xScale(d);
			})
			.attr('y', function(d) {
				return height - yScale(d);
			})
		
		.on('mouseover', function(d, i) {
			tooltip.transition()
				.duration(200)
				.style('opacity', .9)
			tooltip.html(
				'<div>' + d + '<br>' + trans_times[i] + '</div>'
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


	xGuide = d3.select('.barchart svg')
		.append('g')
		.attr('transform', 'translate(' + (margin.left + margin.right) +',' + (height) +')')
		.call(xAxisTicks)

	yGuide = d3.select('.barchart svg')
		.append('g')
		.attr('transform', 'translate(' + (margin.left) + ',0)')
		.call(yAxisTicks)


	// myChart.transition()
	// 	.attr('height', function(d) {
	// 		return yScale(d);
	// 	})
	// 	.attr('y', function(d) {
	// 		return height - yScale(d);
	// 	})
	// 	.delay(function(d, i) {
	// 		return i * 20;
	// 	})
	// 	.duration(1000)
	// 	.ease(d3.easeBounceOut)

}); //end doc