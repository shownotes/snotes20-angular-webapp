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

    $scope.getPodcastTimeline = function () {
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
	 		fillColor : "rgba(151,187,205,0)",
                        strokeColor : "#f1c40f",
                        pointColor : "rgba(151,187,205,0)",
                        pointStrokeColor : "#f1c40f",      
		 }	 
	      ]
	 }

	$scope.timeline.labels = labels;
	$scope.timeline.datasets[0].data = data;
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
                        fillColor : "rgba(151,187,205,0)",
                        strokeColor : "#f1c40f",
                        pointColor : "rgba(151,187,205,0)",
                        pointStrokeColor : "#f1c40f",
                 }
              ]
         }

        $scope.timeline.labels = labels;
        $scope.timeline.datasets[0].data = data;
      });
    }	      
});
