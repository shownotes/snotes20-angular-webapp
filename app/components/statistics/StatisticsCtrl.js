'use strict';

angular.module('snotes30App')
  .controller('StatisticsCtrl', function ($scope, StatisticsService){

      StatisticsService.getWordList().then(function (results){
        $scope.words = results;
      });

      //$scope.words = ["Hallo", "Test", "Lorem", "Ipsum", "Lorem", "ipsum", "dolor", "sit", "amet,", "consetetur", "sadipscing", "elitr,", "sed", "diam", "nonumy", "eirmod", "tempor", "invidunt", "ut", "labore", "et", "dolore", "magna", "aliquyam", "erat,", "sed", "diam"];
      $scope.words = ["holgi","toby","tim","nicolas","gibt","mehr","the","frage","mal","immer","apple","podcast","schon","macht","beim","geht","findet","gut","google","wurde","berlin","neue","holger","uhr","heute","menschen","2","of","frau","ja","kommt","–","album","chat","thema","herr","sendung","martinsen","'s","iphone","leute","musik","intro","twitter","ende","sendungsbeginn","gerne","max","shownotes","mac"];

      $scope.myOnClickFunction = function (element) {
        console.log("click", element);
      }

      $scope.myOnHoverFunction = function (element) {
        console.log("hover", element);
      }

    });
