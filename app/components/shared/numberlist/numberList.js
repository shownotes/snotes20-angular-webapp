'use strict';

angular.module('snotes30App')
.directive('numberList', function() {
  return {
    restrict: 'E',
    replace: false,
    scope: {
      numbers: '='
    },
    templateUrl: 'components/shared/numberlist/numberlist.html',
    controller: function ($scope) {
      $scope.$watch(function (scope) { return scope.numbers; },
        function (newVal, oldVal) {
          if(newVal.length > 2) {
            $scope.subNumbers = newVal.slice(1, newVal.length - 1);
          } else {
            $scope.subNumbers = [];
          }
        }
      );
    }
  };
});
