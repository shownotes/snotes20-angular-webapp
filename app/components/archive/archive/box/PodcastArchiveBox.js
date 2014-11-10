'use strict';

angular.module('snotes30App')
  .directive('archivebox', function() {
    return {
      restrict: 'E',
      replace: true,
      scope: {
        'pod': '='
      },
      templateUrl: '/components/archive/archive/box/podcastarchivebox.html',
      controller: function ($scope, $state) {

      }
    };
  });
