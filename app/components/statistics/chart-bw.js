/* src/chart.js */
// Chart Module
angular.module('myChart', [])

  // D3 Factory
  .factory('d3', function () {

    /* We could declare locals or other D3.js
     specific configurations here. */

    return d3;
  })

  // Scatter Chart Directive
  .directive('myScatterChart', ["d3",
    function (d3) {

      function draw(svg, width, height, data) {
        svg
          .attr('width', width)
          .attr('height', height);

        // Define a margin
        var margin = 30;

        // Define x scale
        var xScale = d3.time.scale()
          .domain([
            d3.min(data, function (d) {
              return d.time;
            }),
            d3.max(data, function (d) {
              return d.time;
            })
          ])
          .range([margin, width - margin]);

        // Define x-axis
        var xAxis = d3.svg.axis()
          .scale(xScale)
          .orient('top')
          .tickFormat(d3.time.format('%S'));

        // Define y-scale
        var yScale = d3.time.scale()
          .domain([0, d3.max(data, function (d) {
            return d.visitors;
          })])
          .range([margin, height - margin]);

        // Define y-axis
        var yAxis = d3.svg.axis()
          .scale(yScale)
          .orient('left')
          .tickFormat(d3.format('f'));

        // Draw the x-axis
        svg.select('.x-axis')
          .attr("transform", "translate(0, " + margin + ")")
          .call(xAxis);

        // Draw the y-axis
        svg.select('.y-axis')
          .attr("transform", "translate(" + margin + ")")
          .call(yAxis);

        // Add new the data points
        svg.select('.data')
          .selectAll('circle').data(data)
          .enter()
          .append('circle');

        // Updated all data points
        svg.select('.data')
          .selectAll('circle').data(data)
          .attr('r', 2.5)
          .attr('cx', function (d) {
            return xScale(d.time);
          })
          .attr('cy', function (d) {
            return yScale(d.visitors);
          });
      }

      return {
        restrict: 'E',
        scope: {
          data: '='
        },
        compile: function (element, attrs, transclude) {

          // Create a SVG root element
          var svg = d3.select(element[0]).append('svg');

          svg.append('g').attr('class', 'data');
          svg.append('g').attr('class', 'x-axis axis');
          svg.append('g').attr('class', 'y-axis axis');

          // Define the dimensions for the chart
          var width = 600, height = 300;

          // Return the link function
          return function (scope, element, attrs) {
            // Watch the data attribute of the scope
            scope.$watch('data', function (newVal, oldVal, scope) {
              // Update the chart
              draw(svg, width, height, scope.data);
            }, true);
          };
        }
      };
    }]);

