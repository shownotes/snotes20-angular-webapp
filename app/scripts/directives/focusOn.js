'use strict';

angular.module('snotes20App').directive('focusOn', function() {
  return function($scope, elem, attr) {
    $scope.$watch('modeRegister', function(e) {
      if($scope.modeRegister)
        elem[0].focus();
    });
  };
});