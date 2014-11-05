'use strict';

angular.module('snotes30App')
.controller('DocumentSightingCtrl', function ($scope, $rootScope, doc, DocumentService) {
  $scope.doc = doc;
  $scope.episode = doc.episode;
});
