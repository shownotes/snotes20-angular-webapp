'use strict';

angular.module('snotes30App')
  .controller('ImportStatusCtrl', function ($scope, $location, Restangular) {
    $scope.logs = [];

    Restangular.all('importerlogs').getList().then(
      function (logs) {
        $scope.logs = logs;
      }
    );
  });
