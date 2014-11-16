'use strict';

angular.module('snotes30App')
  .controller('ArchiveSearchCtrl', function ($scope, $stateParams, ArchiveService) {
    $scope.searchterm = $stateParams.q;
    ArchiveService.search($stateParams.q).then(function (results) {
      $scope.results = results;
    })
  });
