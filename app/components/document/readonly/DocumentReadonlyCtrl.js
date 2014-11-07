'use strict';

angular.module('snotes30App')
  .controller('DocumentReadonlyCtrl', function ($scope, docname, doc) {
    $scope.doc = doc;
    $scope.episode = doc.episode;
});
