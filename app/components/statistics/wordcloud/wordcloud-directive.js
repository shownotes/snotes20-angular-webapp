'use strict';

angular.module('myChart')
  .directive('wordcloud', ['d3', function (d3) {
    return {
      restrict: 'E',
      scope: {
        // attributes
        width: "@",
        height: "@",
        fontFamily: "@",
        fontSize: "@",

        // Bindings
        words: "=",

        // EventCallbacks
        onClick: "&",
        onHover: "&"
      },
      link: function postLink(scope, element, attrs) {
        scope.$watch('words', function () {
          // Default Values
          var width = 800;
          var height = 600;
          var fontFamily = "Impact";
          var fontSize = 100;
          var words;

          // Check and set attributes, else keep then default values
          if (angular.isDefined(attrs.fontSize)) fontSize = attrs.fontSize * 1 || 0; // !parseInt, detect wrong input
          if (angular.isDefined(attrs.width))        width = attrs.width;
          if (angular.isDefined(attrs.height)) {
            fontSize = Math.sqrt((attrs.height / height)) * fontSize;
            height = attrs.height;
          }
          if (angular.isDefined(attrs.fontFamily))   fontFamily = attrs.fontFamily;

          // Check Scope
          if (angular.isDefined(scope.words))    words = scope.words;

          // Skip rendering when no corrent word param is parsed
          if (angular.isDefined(scope.words) && angular.isArray(words)) {
            words = scope.words
          }
          else if (angular.element(element).find("word").length > 0) {
            var subelements = angular.element(element).find("word");
            words = [];
            angular.forEach(subelements, function (word) {
              words.push(angular.element(word).text());
              angular.element(word).remove();
            });
          }
          else if (element.text().length > 0) {
            // if no words are submitted
            return;
          }
          else {
            element.text("wordcloud: Please define some words");
            return;
          }
          // Font-Size Param wrong
          if (!angular.isNumber(fontSize) || fontSize <= 0) {
            element.text("wordcloud: font-size attribute not valid. font-size " + attrs.fontSize + " -> " + fontSize);
            return;
          }


          var cloudFactory = function (words) {

            var fill = d3.scale.category20();

            var largest_frequency = words[0]["frequency"];

            d3.layout.cloud().size([width, height])
              .words(words.map(function (d) {
                var freq = Math.sqrt(d["frequency"] / largest_frequency);
                return {text: d["word"], size: freq * fontSize};
              }))
              .rotate(function () {
                //return ~~(Math.random() * 2) * -90;
                return (~~(Math.random() * 6) - 3) * 15;
              })
              .font(fontFamily)
              .fontSize(function (d) {
                return d.size;
              })
              .on("end", draw)
              .start();

            function draw(words) {
              // Center the drawing
              var height_translate = height / 2;
              var width_translate = width / 2;
              var rootElement = element[0];


              d3.select(rootElement)
                .append("svg")
                .attr("width", width)
                .attr("height", height)
                .append("g")
                .attr("transform", "translate(" + width_translate + "," + height_translate + ")")// Translate to center
                .selectAll("text")
                .data(words)
                .enter().append("text")
                .style("font-size", function (d) {
                  return d.size + "px";
                })
                .style("font-family", fontFamily)
                .style("fill", function (d, i) {
                  return fill(i);
                })
                .attr("text-anchor", "middle")
                .attr("transform", function (d) {
                  return "translate(" + [d.x, d.y] + ") rotate(" + d.rotate + ")";
                })
                .text(function (d) {
                  return d.text;
                })
                .on("click", function (d) {
                  scope.onClick({element: d});
                })
                .on("mouseover", function (d) {
                  scope.onHover({element: d});
                });
            }
          };

          // Execute
          cloudFactory(words);
        });
      }
    };
  }]);
