'use strict';

angular.module('snotes30App')
  .controller('DocumentReadonlyCtrl', function ($scope, $stateParams, doc) {
    $scope.doc = doc;
    $scope.episode = doc.episode;
    $scope.pub = $stateParams.pub;
});
