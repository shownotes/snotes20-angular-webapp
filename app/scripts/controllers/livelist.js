'use strict';

angular.module('snotes30App')
  .controller('LiveListCtrl', function ($scope, $location, Restangular, DocumentService) {
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
      DocumentService.createFromEpisode(ep).then(function (doc) {
        $location.path('/doc/' + doc.name);
      });
    };
  });
