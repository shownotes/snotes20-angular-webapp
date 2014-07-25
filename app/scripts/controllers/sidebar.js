'use strict';

angular.module('snotes30App')
  .controller('SidebarController', function ($scope, $cookies, $location, AuthenticationService, Restangular) {

    $scope.loginform = {
      status: 'up',
      mode: 'login'
    };

    $scope.errors = {};

    AuthenticationService.injectMe($scope);

    function flipFormMode() {
      $scope.loginform.mode = $scope.loginform.mode === 'login' ? 'register' : 'login';
    }

    function handleLoginRegister (mode, func) {
      $scope.loginform.errors = [];
      
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
      $scope.loginform.promise = AuthenticationService.login(
        $scope.user.username,
        $scope.user.password
      ).then(function (user) {
        $scope.currentUser = {
          username: $scope.user.username
        };
        $scope.user = null;
        if(!user.migrated) {
          $location.url('/user/upgrade');
        }
        if($location.url().indexOf('/user/activate') === 0) {
          $location.url('/');
        }
      }, function (errors) {
        $scope.loginform.errors = { 'loginfailed': true };
      });
    }

    function doRegister() {
      $scope.loginform.promise = AuthenticationService.register(
        $scope.user.username,
        $scope.user.email,
        $scope.user.password
      ).then(function () {
        flipFormMode();
        $location.url('/user/registration');
      }, function (errors) {
        $scope.loginform.errors = errors.data;
      });
    }

    $scope.logout = function () {
      AuthenticationService.logout().then(function () {
        $scope.currentUser = null;
      });
    };

    $scope.requestPwReset = function () {
      Restangular.one('users', $scope.user.username).customPOST({}, 'request_pw_reset').then(function () {
        $scope.pwresetdone = true;
      });
    };
  });
