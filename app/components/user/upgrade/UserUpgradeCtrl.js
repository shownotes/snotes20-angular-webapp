'use strict';

angular.module('snotes30App')
  .controller('UserUpgradeCtrl', function ($scope, $location, Restangular, AuthenticationSvc) {

    AuthenticationSvc.injectMe($scope);

    $scope.doUpgrade = function () {
      Restangular.one('users', 'me').customPOST({password: $scope.upgrade.password}, "upgrade").then(function () {
        $location.url('/');
      }, function () {
        alert("nope")
      })
    };
  });
