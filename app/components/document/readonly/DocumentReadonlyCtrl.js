'use strict';

angular.module('snotes30App')
  .controller('DocumentReadonlyCtrl', function ($scope, $stateParams, docname, doc) {
    $scope.doc = doc;
    $scope.episode = doc.episode;
    $scope.pub = $stateParams.pub;
});
