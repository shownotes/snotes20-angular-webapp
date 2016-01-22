'use strict';

angular.module('snotes30App')
  .controller('StatisticsCtrl', ['$scope', 'Restangular',
    function ($scope, Restangular) {

      $scope.word = Restangular.all('statistic', 'wordfrequency', '?top=200').getList();
      $scope.words = ["Hallo", "Test", "Lorem", "Ipsum", "Lorem", "ipsum", "dolor", "sit", "amet,", "consetetur", "sadipscing", "elitr,", "sed", "diam", "nonumy", "eirmod", "tempor", "invidunt", "ut", "labore", "et", "dolore", "magna", "aliquyam", "erat,", "sed", "diam"];

      $scope.myOnClickFunction = function (element) {
        console.log("click", element);
      }

      $scope.myOnHoverFunction = function (element) {
        console.log("hover", element);
      }

    }]);
