'use strict';

angular.module('snotes30App')
  .controller('UserUpgradeCtrl', function ($scope, $rootScope, $location, Restangular, AuthenticationSvc) {

    AuthenticationSvc.injectMe($scope);

    $scope.doUpgrade = function () {
      Restangular.one('users', 'me').customPOST({password: $scope.upgrade.password}, "upgrade").then(function () {
        AuthenticationSvc.injectMe($rootScope);
        $location.url('/');
      }, function () {
        alert("nope")
      })
    };
  });
