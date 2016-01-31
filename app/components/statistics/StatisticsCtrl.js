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

  });
