'use strict';

angular.module('snotes30App')
  .service('AuthenticationSvc', function ($rootScope, $q, Restangular) {
    var auth = Restangular.all('auth');
    var users = Restangular.all('users');

    this.login = function (username, password) {
      return auth.post({
        username: username,
        password: password
      });
    };

    this.logout = function () {
      return auth.customDELETE('me');
    };

    this.getStatus = function () {
      return auth.customGET('');
    };

    this.injectMe = function (scope) {
      this.getStatus().then(function (rtn) {
        scope.currentUser = rtn.user;
      });
    };

    this.register = function (username, email, password) {
      return users.post({
        username: username,
        email: email,
        password: password
      });
    };
  });
