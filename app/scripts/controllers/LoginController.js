'use strict';

angular.module('snotes20App')
  .controller('LoginController', function ($scope, $rootScope, LoginService) {
    $scope.login = function () {
      var username = $scope.username;
      var password = $scope.password;

      LoginService.login(username, password).then(
        function (user)
        {
          $rootScope.user = user;
          $scope.username = "";
          $scope.password = "";
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
