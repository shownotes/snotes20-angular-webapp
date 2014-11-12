'use strict';

angular.module('snotes30App')
.directive('mediaImage', function() {
  return {
    restrict: 'E',
    replace: true,
    scope: {
      path: '='
    },
    template: '<img src="{{url}}"/>',
    controller: function ($scope, CONFIG) {
      $scope.url = CONFIG.mediaUrl + '/' + ($scope.path || 'cover-placeholder.png');
    }
  };
});
