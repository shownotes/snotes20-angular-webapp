'use strict';

angular.module('snotes30App')
  .controller('UserPwResetCtrl', function ($scope, $routeParams, Restangular, actionStatusGlueService) {

    $scope.sendPwReset = function () {
      var data = {
        username: $routeParams.username,
        token: $routeParams.token,
        password: $scope.pwreset.password
      };

      var stat = actionStatusGlueService.fac($scope.pwreset);

      Restangular.one('users', data.username)
                 .customPOST(data, 'pw_reset')
                 .then(stat.resolve, stat.reject).finally(stat.reset());
    };
  });
