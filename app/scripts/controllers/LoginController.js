'use strict';

angular.module('snotes20App')
  .controller('LoginController', function ($scope, $rootScope) {
    $scope.login = function () {
      $rootScope.isLoggedIn = true;
    };

    $scope.register = function () {
      if(!$rootScope.modeRegister) {
        $rootScope.modeRegister = true;
      } else {
        // send to server..
        $rootScope.modeRegister = false;
      }
    };

    $scope.logout = function () {
      $rootScope.isLoggedIn = false;
    };
  });
