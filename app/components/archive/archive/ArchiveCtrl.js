'use strict';

angular.module('snotes30App')
  .controller('ArchiveCtrl', function ($scope, podcasts, recentpodcasts) {
    $scope.podcasts = podcasts;
    $scope.recentpodcasts = recentpodcasts;
  });
