'use strict';

angular.module('snotes30App')
  .controller('UserPwResetCtrl', function ($scope, $routeParams, Restangular) {

    $scope.sendPwReset = function () {
      var data = {
        username: $routeParams.username,
        token: $routeParams.token,
        password: $scope.password
      };

      Restangular.one('users', data.username).customPOST(data, 'pw_reset').then(function () {
        $scope.success = true;
      }, function () {
        $scope.success = false;
      })
    };
  });
