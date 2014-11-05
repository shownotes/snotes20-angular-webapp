'use strict';

angular.module('snotes30App')
  .controller('UserActivateCtrl', function ($scope, $routeParams, $location, Restangular) {
    var data = {
      username: $routeParams.username,
      token: $routeParams.token
    };

    if($location.url().indexOf('/user/confirm/') === 0)
      $scope.mode = 'email';
    else
      $scope.mode = 'account';

    Restangular.one('users', data.username).customPOST(data, 'activate').then(function () {
      $scope.success = true;
    }, function () {
      $scope.success = false;
    })
  });
