'use strict';

angular.module('snotes30App')
  .controller('PublicProfileCtrl', function ($scope, $stateParams, AuthenticationSvc, Restangular) {
    var user = Restangular.one('users', $stateParams.username);

    $scope.user = {};

    user.get().then(function (user) {
      $scope.user = user;

      var last_login = +new Date() - +new Date($scope.user.date_login);
      var day = 60 * 60 * 24 * 1000;
      var days = last_login / day;

      if(days <= 1) {
        $scope.last_login = "zuletzt heute";
      } else if(days <= 2) {
        $scope.last_login = "zuletzt gestern";
      } else if(days <= 3) {
        $scope.last_login = "zuletzt vorgestern";
      } else if(days > 3 && days < 7) {
        $scope.last_login = "zuletzt vor " + (~~days) + " Tagen";
      } else if(days >= 7 && days <= 10) {
        $scope.last_login = "zuletzt vor einer Woche";
      } else {
        $scope.last_login = "schon länger nicht";
      }

    }, function () {
      $scope.user = null;
    });

    AuthenticationSvc.getStatus().then(function (data) {
      $scope.currentUser = data.user;
    });
  });
