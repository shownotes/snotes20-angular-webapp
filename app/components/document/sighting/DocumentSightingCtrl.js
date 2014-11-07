'use strict';

angular.module('snotes30App')
.controller('DocumentSightingCtrl', function ($scope, $rootScope, $q, doc, DocumentService) {
  $scope.doc = doc;

  $scope.publication = {
    episode: doc.episode,
    podcasters: [],
    shownoters: []
  };

  $scope.epnumber = doc.episode.number;

  $scope.editorMode = 'preview';

  $scope.switchEditorMode = function (mode) {
    $scope.editorMode = mode;
  };

  $scope.addShownoter = function (shownoter) {
    var deferred = $q.defer();

    $scope.publication.shownoters.push(shownoter);

    deferred.resolve();
    return deferred.promise;
  };

  $scope.addPodcaster = function (podcaster) {
    var deferred = $q.defer();

    $scope.publication.podcasters.push(podcaster);

    deferred.resolve();
    return deferred.promise;
  };
});
