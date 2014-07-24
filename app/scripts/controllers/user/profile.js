'use strict';

angular.module('snotes30App')
  .controller('UserProfileCtrl', function ($scope, Restangular, actionStatusGlueService) {
    var me = Restangular.one('users', 'me');

    var reloadMe = function () {
      me.get().then(function (user) {
        $scope.user = user;
      });
    };

    var patchMe = function (obj, statobj, action) {
      var stat = actionStatusGlueService.fac(statobj);
      me.patch(obj, { action: action })
        .then(stat.resolve, stat.reject)
        .then(reloadMe)
        .finally(stat.reset());
    };

    reloadMe();

    $scope.colorbio = {};
    $scope.socials = {};

    $scope.saveBioColor = function () {
      var color = $scope.user.color;

      if(color[0] === "#")
        color = color.substr(1).toUpperCase();

      patchMe({
        'color': color,
        'bio': $scope.user.bio
      }, $scope.colorbio, 'colorbio');
    };

    $scope.saveSocials = function () {
      patchMe({
        'socials': $scope.user.socials
      }, $scope.socials, 'socials');
    };

    $scope.changeMail = function () {
      patchMe({
        'email': $scope.changemail.email,
        'password': $scope.changemail.password
      }, $scope.changemail, 'email');
    };

    $scope.changePassword = function () {
      patchMe({
        'password': $scope.pwchange.password,
        'newpassword': $scope.pwchange.newpassword
      }, $scope.pwchange, 'password');
    };
  });
