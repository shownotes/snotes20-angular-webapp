'use strict';

angular.module('snotes30App')
  .controller('UserUpgradeCtrl', function ($scope, $rootScope, $location, Restangular, AuthenticationSvc, actionStatusGlueService) {
    $scope.upgradeStatus = {};
    $scope.upgrade = {};

    AuthenticationSvc.injectMe($scope);

    $scope.doUpgrade = function () {
      var stat = actionStatusGlueService.fac($scope.upgradeStatus);
      Restangular.one('users', 'me').customPOST({password: $scope.upgrade.password}, "upgrade").then(function () {
        AuthenticationSvc.injectMe($rootScope);
        $location.url('/');
      }, stat.reject);
    };
  });
