'use strict';

angular.module('snotes30App')
.directive('nameList', function() {
  return {
    restrict: 'E',
    replace: true,
    scope: {
      names: '=',
      addName: '=',
      delName: '=',
      nameAttr: '@'
    },
    templateUrl: 'components/shared/namelist/namelist.html',
    controller: function ($scope) {
      $scope.add = function () {
        var obj = {};

        obj[$scope.nameAttr] = $scope.newName;

        $scope.addName(obj).then(function () {
          $scope.newName = '';
        });
      };

      $scope.delete = function (obj) {
        $scope.delName(obj);
      };
    }
  };
});
