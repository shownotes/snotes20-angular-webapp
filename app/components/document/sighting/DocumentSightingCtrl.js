'use strict';

angular.module('snotes30App')
.controller('DocumentSightingCtrl', function ($scope, $rootScope, $q, doc, DocumentService) {
  $scope.doc = doc;
  $scope.episode = doc.episode;

  $scope.helpers = [];

  $scope.podcasters = [];

  $scope.editorMode = 'preview';

  $scope.switchEditorMode = function (mode) {
    $scope.editorMode = mode;
  };

  $scope.addHelper = function (name) {
    var deferred = $q.defer();

    $scope.helpers.push({
      name: name
    });

    deferred.resolve();
    return deferred.promise;
  };

  $scope.addPodcaster = function (name) {
    var deferred = $q.defer();

    $scope.podcasters.push({
      name: name
    });

    deferred.resolve();
    return deferred.promise;
  };
});
