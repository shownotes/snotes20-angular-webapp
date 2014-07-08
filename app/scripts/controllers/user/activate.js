'use strict';

angular.module('snotes30App')
  .controller('UserActivateCtrl', function ($scope, $routeParams, Restangular) {
    var data = {
      username: $routeParams.username,
      token: $routeParams.token
    };

    Restangular.one('users', data.username).customPOST(data, 'activate').then(function () {
      $scope.success = true;
    }, function () {
      $scope.success = false;
    })
  });
