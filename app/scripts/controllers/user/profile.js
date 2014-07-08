'use strict';

angular.module('snotes30App')
  .controller('UserProfileCtrl', function ($scope, Restangular) {
    var me = Restangular.one('users', 'me');

    $scope.user = { };

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
  });
