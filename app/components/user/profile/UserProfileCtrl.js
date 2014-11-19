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
        .finally(stat.reset);
    };

    reloadMe();

    $scope.colorbio = {};
    $scope.socials = {};

    $scope.luminosity = function(color) {
      // based on etherpad-lite (apache)
      // https://github.com/ether/etherpad-lite/blob/7b9fd81284a6e2191d007769c899907ea3f64232/src/static/js/colorutils.js#L111-L115

      var c = [
        parseInt(color.substr(0, 2), 16) / 255,
        parseInt(color.substr(2, 2), 16) / 255,
        parseInt(color.substr(4, 2), 16) / 255
      ];

      return c[0] * 0.30 + c[1] * 0.59 + c[2] * 0.11;
    };

    $scope.colorOkay = function () {
      return $scope.luminosity($scope.getColor()) >= 0.5;
    };

    $scope.getColor = function () {
      if(!$scope.user)
        return "000000";

      var color = $scope.user.color;

      if(color[0] === "#")
        color = color.substr(1).toUpperCase();

      return color;
    };

    $scope.saveBioColor = function () {
      patchMe({
        'color': $scope.getColor(),
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
