'use strict';

angular.module('snotes30App')
  .controller('ProfileCtrl', function ($scope, Restangular) {
    $scope.user = {
      username: 'Gurkenluto'
    };
  });
