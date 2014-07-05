'use strict';

angular.module('snotes30App')
  .controller('DocumentCtrl', function ($scope, $routeParams, Restangular) {
    $scope.name = $routeParams.name;
  });
