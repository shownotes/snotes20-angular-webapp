'use strict';

angular.module('snotes20App')
  .controller('LoginController', function ($scope, $rootScope) {
    $scope.login = function () {
      $rootScope.isLoggedIn = true;
    };

    $scope.register = function () {
      if(!$scope.modeRegister) {
        $scope.modeRegister = true;
      } else {
        // send to server..
        $scope.modeRegister = false;
      }
    };

    $scope.logout = function () {
      $rootScope.isLoggedIn = false;
    };
  });
