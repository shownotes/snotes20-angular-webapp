'use strict';

angular.module('snotes30App')
  .controller('StatisticsCtrl', function ($scope, $location, StatisticsService){

      $scope.getWords = function (){
       StatisticsService.getWordList().then(function (results){
          $scope.words = results;
        });
      }

    $scope.getPodcastWords = function (slug){
      console.log("slug", slug);
      StatisticsService.getPodcastWordList(slug).then(function (results){
        $scope.words = results;
      });
    }

      $scope.myOnClickFunction = function (element) {
        console.log("click", element.text);
        $location.url('/archive/search/?q=' + element.text);
      }

      $scope.myOnHoverFunction = function (element) {
        console.log("hover", element);
      }

    });
