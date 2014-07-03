'use strict';

angular.module('snotes30App')
  .controller('SidebarController', function ($scope, $cookies, AuthenticationService) {

    $scope.loginform = {
      status: 'up',
      mode: 'login'
    };

    $scope.errors = {};

    AuthenticationService.getStatus().then(function (user) {
      $scope.currentUser = user;
    });

    function flipFormMode() {
      $scope.loginform.mode = $scope.loginform.mode === 'login' ? 'register' : 'login';
    }

    function handleLoginRegister (mode, func) {
      if($scope.loginform.mode !== mode) {
        flipFormMode();
      } else if($scope.loginform.frm.$valid) {
        func();
      }
    }

    $scope.login = function () {
      handleLoginRegister('login', doLogin);
    };

    $scope.register = function () {
      handleLoginRegister('register', doRegister);
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
