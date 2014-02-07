'use strict';

angular.module('snotes20App')
  .controller('LoginController', function ($scope, $rootScope, LoginService) {

    $scope.reset = function () {
      $scope.username = '';
      $scope.email = '';
      $scope.password = '';
      $scope.password2 = '';
    };

    $scope.login = function () {
      var username = $scope.username;
      var password = $scope.password;

      LoginService.login(username, password).then(
        function (user)
        {
          $rootScope.user = user;
          $scope.reset();
        },
        function ()
        {
          $rootScope.user = null;
        }
      );
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
      LoginService.logout().then(
        function () { $rootScope.user = null; },
        function () { }
      );
    };
  });
