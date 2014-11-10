'use strict';

angular.module('snotes30App')
  .controller('LiveListCtrl', function ($scope, $state, $timeout, Restangular, DocumentService) {
    $scope.episodes = [];

    Restangular.all('soonepisodes').getList().then(
      function (episodes) {
        $scope.episodes = episodes;
      }
    );

    $scope.isPast = function (ep) {
      var today = new Date().setHours(0,0,0,0);
      return ep.date < today;
    };

    $scope.openDoc = function (ep) {
      var name = (typeof ep === 'string') ? ep : ep.document.name;
      $state.go('document-edit', { name: name }, { inherit: false });
    };

    $scope.create = function (index, nonumber) {
      var ep = $scope.episodes[index];

      if(ep.number || nonumber) {
        var _doc;
        DocumentService.createFromEpisode(ep).then(function (doc) {
          _doc = doc;
          return DocumentService.setNumber(doc, ep.number);
        }).then(function () {
          $scope.openDoc(_doc.name);
        });
      } else {
        $scope.setNumber = ep;
        $timeout(function () { angular.element("#addNumber_" + index).focus(); }, 0);
      }
    };
  });
