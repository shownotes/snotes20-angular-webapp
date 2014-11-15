'use strict';

angular.module('snotes30App')
  .controller('UserPwResetCtrl', function ($scope, $stateParams, Restangular, actionStatusGlueService) {
    $scope.username = $stateParams.username;

    $scope.sendPwReset = function () {
      var data = {
        username: $stateParams.username,
        token: $stateParams.token,
        password: $scope.pwreset.password
      };

      var stat = actionStatusGlueService.fac($scope.pwreset);

      Restangular.one('users', data.username)
                 .customPOST(data, 'pw_reset')
                 .then(stat.resolve, stat.reject).finally(stat.reset());
    };
  });
