'use strict';

angular.module('snotes30App')
  .controller('UserProfileCtrl', function ($scope, Restangular) {
    $scope.user = {
      username: 'Gurkenluto'
    };
  });
