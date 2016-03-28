'use strict';

angular.module("snotes30App")
  .controller("BarCtrl", function ($scope) {

    $scope.chart = {
    	labels : ["09.2015", "12.2015", "01.2016", "02.2106", "03.2016"],
     	datasets : [
        	{
                   	fillColor : "rgba(151,187,205,0)",
            		strokeColor : "#f1c40f",
            		pointColor : "rgba(151,187,205,0)",
            		pointStrokeColor : "#f1c40f",
            		data : [8, 3, 2, 5, 4]
       	 	}
    	], 
     };  
});

