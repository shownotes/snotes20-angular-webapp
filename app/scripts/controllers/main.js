'use strict';

/**
 * @ngdoc function
 * @name snotes30App.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the snotes30App
 */
angular.module('snotes30App')
  .controller('MainCtrl', function ($scope, Restangular) {
    $scope.episodes = [];

    Restangular.all('soonepisodes').getList().then(
      function (episodes) {
        $scope.episodes = episodes;
      }
    );
  });
