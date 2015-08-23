'use strict';

angular.module('snotes30App')
  .controller('DocumentReadonlyCtrl', function ($scope, $stateParams, $location, $state, doc) {
    $scope.doc = doc;
    $scope.episode = doc.episode;
    $scope.pub = $stateParams.pub;
    $scope.docEditUrl = $state.href('document-edit', { name: doc.name }, {absolute: true});
});
