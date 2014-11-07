'use strict';

angular.module('snotes30App')
  .controller('LiveListCtrl', function ($scope, $state, Restangular, DocumentService) {
    $scope.episodes = [];

    Restangular.all('soonepisodes').getList().then(
      function (episodes) {
        $scope.episodes = episodes;
      }
    );

    $scope.openDoc = function (ep) {
      $state.go('document-edit', { name: ep.document.name }, { inherit: false });
    };

    $scope.create = function (ep) {
      DocumentService.createFromEpisode(ep).then(function (doc) {
        $scope.openDoc(doc.name);
      });
    };
  });
