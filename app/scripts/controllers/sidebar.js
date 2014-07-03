'use strict';

angular.module('snotes30App')
  .controller('SidebarController', function ($scope, $cookies, AuthenticationService) {

    $scope.loginform = {
      isDown: false,
      mode: 'login'
    };

    $scope.errors = {};

    AuthenticationService.getStatus().then(function (user) {
      $scope.currentUser = user;
    });

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
        $scope.user.username,
        $scope.user.password
      ).then(function () {
        $scope.currentUser = {
          username: $scope.user.username
        };
        $scope.user = null;
      });
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
        $scope.user.username,
        $scope.user.email,
        $scope.user.password
      );
    }

    $scope.logout = function () {
      AuthenticationService.logout().then(function () {
        $scope.currentUser = null;
      });
    };
  });
