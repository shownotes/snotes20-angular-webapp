'use strict';

angular.module('snotes30App')
  .config(['ChartJsProvider', function (ChartJsProvider) {
	 // Configure all charts
	 ChartJsProvider.setOptions({
	         colours: ['#b6e7fb', '#e6f7fe'],
	         responsive: false
	  });
	  // Configure all line charts
	  ChartJsProvider.setOptions('Line', {
	         datasetFill: false
	  });
   }])
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
      StatisticsService.getPodcastTimeline().then(function (results) {
	 var labels = new Array();
	 var data = new Array();

	 for (var i = 0; i < results.length; i++) {
    	     labels.push(results[i][1]);
	     data.push(results[i][0]);
	 }

	$scope.data = new Array();
	$scope.data.push(data);
	$scope.labels = labels;
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

	 $scope.data = new Array();
	 $scope.data.push(data);
	 $scope.labels = labels;
      });
    }
    
    $scope.onClick = function (points, evt) {
      var param = (typeof points != 'undefined' && typeof points[0] != 'undefined' && typeof points[0].label != 'undefined') ? points[0].label : '';
      $location.url('/archive/?period=' + param);
      $scope.$apply();
    };
});
