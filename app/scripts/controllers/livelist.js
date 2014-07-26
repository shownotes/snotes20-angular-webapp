'use strict';

angular.module('snotes30App')
  .controller('LiveListCtrl', function ($scope, $location, Restangular, DocumentService) {
    $scope.episodes = [];

    Restangular.all('soonepisodes').getList().then(
      function (episodes) {
        $scope.episodes = episodes;
      }
    );

    function docurl (name) { return '/doc/' + name; }
    $scope.docurl = docurl;

    $scope.create = function (ep) {
      DocumentService.createFromEpisode(ep).then(function (doc) {
        $location.path(docurl(doc.name));
      });
    };
  });
