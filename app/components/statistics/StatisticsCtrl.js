'use strict';

angular.module('snotes30App')
  .controller('StatisticsCtrl', function ($scope, $location, StatisticsService) {

    $scope.getWords = function () {
      StatisticsService.getWordList().then(function (results) {
        $scope.words = results;
      });
    }

    $scope.getPodcastWords = function (slug) {
      StatisticsService.getPodcastWordList(slug).then(function (results) {
        $scope.words = results;
      });
    }

    $scope.getWordsFreq = function () {
      StatisticsService.getWordListFreq().then(function (results) {
        $scope.words = results;
      });
    }

    $scope.getPodcastWordsFreq = function () {
      StatisticsService.getPodcastWordListFreq($scope.podcast.slug).then(function (results) {
        $scope.words = results;
      });
    }

    $scope.myOnClickFunction = function (element) {
      $location.url('/archive/search/?q=' + element.text);
      $scope.$apply();
    }

    $scope.myOnHoverFunction = function (element) {
      console.log("hover", element);
    }

    $scope.getPodcastTimeline = function (label) {
	    console.log("qual o resultado do label", label);
      StatisticsService.getPodcastTimeline().then(function (results) {
	 var labels = new Array();
	 var data = new Array();

	 for (var i = 0; i < results.length; i++) {
    	     labels.push(results[i][1]);
	     data.push(results[i][0]);
	 }

         $scope.timeline = {
      	     datasets : [
	         {
	 		fillColor : "#e6f7fe",
                        strokeColor : "#b6e7fb",
                        pointColor : "#e6f7fe",
                        pointStrokeColor : "#b6e7fb",      
		 }	 
	      ]
	 }

	$scope.timeline.labels = labels;
	$scope.timeline.datasets[0].data = data;
	$scope.data = new Array();
	$scope.data.push(data);
	$scope.labels = labels;
	$scope.series = ['Series A'];
	console.log("scope", $scope);
      });
    }

    $scope.getEpisodeTimeline = function (slug) {
      StatisticsService.getEpisodeTimeline(slug).then(function (results) {
         var labels = new Array();
         var data = new Array();

         for (var i = 0; i < results.length; i++) {
             labels.push(results[i][1]);
             data.push(results[i][0]);
         }

         $scope.timeline = {
             datasets : [
                 {
                        fillColor : "#fbedb6",
                        strokeColor : "#f1c40f",
                        pointColor : "#fbedb6",
                        pointStrokeColor : "#f1c40f",
                 }
              ]
         }

        $scope.timeline.labels = labels;
        $scope.timeline.datasets[0].data = data;
      });
    }
    
    $scope.onClick = function (points, evt) {
      var param = (typeof points[0].label != 'undefined') ? points[0].label : '';
      $location.url('/archive/?period=' + param);
      $scope.$apply();
    };
});
