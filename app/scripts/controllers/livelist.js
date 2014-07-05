'use strict';

angular.module('snotes30App')
  .controller('LiveListCtrl', function ($scope, $location, Restangular) {
    $scope.episodes = [];

    Restangular.all('soonepisodes').getList().then(
      function (episodes) {
        $scope.episodes = episodes;
      }
    );

    $scope.join = function (ep) {
      $location.path('/doc/' + ep.document.name);
    };

    $scope.create = function (ep) {
      $location.path('/doc/' + ep.document.name);
    };
  });
