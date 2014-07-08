'use strict';

angular.module('snotes30App')
  .controller('UserProfileCtrl', function ($scope, Restangular) {
    var me = Restangular.one('users', 'me');

    var reloadMe = function () {
      me.get().then(function (user) {
        $scope.user = user;
      });
    };

    reloadMe();

    $scope.saveBioColor = function () {
      me.patch({
        'color': $scope.user.color.substr(1).toUpperCase(),
        'bio': $scope.user.bio
      }).then(reloadMe);
    };

    $scope.changeMail = function () {
      me.patch({
        'email': $scope.changemail.email,
        'password': $scope.changemail.password
      }).then(function () {
        $scope.changemail = { success: true };
      }, function () {
        $scope.changemail = { fail: true };
      }).then(reloadMe);
    };

    $scope.changePassword = function () {
      me.patch({
        'password': $scope.pwchange.password,
        'newpassword': $scope.pwchange.newpassword
      }).then(function () {
        $scope.pwchange = { success: true };
      }, function () {
        $scope.pwchange = { fail: true };
      }).then(reloadMe);
    };


  });
