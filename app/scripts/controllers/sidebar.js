'use strict';

angular.module('snotes30App')
  .controller('SidebarController', function ($scope, AuthenticationService) {

    $scope.loginform = {
      isDown: false,
      mode: 'login'
    };

    $scope.errors = {};

    function flipFormMode() {
      $scope.loginform.mode = $scope.loginform.mode === 'login' ? 'register' : 'login';
    }

    $scope.login = function () {
      if($scope.loginform.mode === 'register') {
        flipFormMode();
      } else {
        doLogin();
      }
    };

    function doLogin() {
      AuthenticationService.login(
        $scope.username,
        $scope.password
      );
    }

    $scope.register = function () {
      if($scope.loginform.mode === 'login') {
        flipFormMode();
      } else {
        doRegister();
      }
    };

    function doRegister() {
      AuthenticationService.register(
        $scope.username,
        $scope.email,
        $scope.password
      );
    }

  });
