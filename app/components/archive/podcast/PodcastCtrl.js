'use strict';

angular.module('snotes30App')
  .controller('ArchivePodcastCtrl', function ($scope, podcast) {
    $scope.podcast = podcast;

    $scope.hasPub = function () {
      return function (item) {
        return item.publications.length > 0;
      }
    };

    $scope.getPub = function (ep) {
      return ep.publications[ep.publications.length - 1];
    }
  });
