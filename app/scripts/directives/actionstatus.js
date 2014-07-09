'use strict';

angular.module('snotes30App').directive('actionStatus', function() {
  return {
    restrict: 'E',
    scope: {
      successText: '@',
      failText: '@',
      loadingText: '@',
      active: '=',
      status: '='
    },
    compile: function (element, attrs) {
      if(!attrs.loadingText) attrs.loadingText = "Bitte warten..."
    },
    template: '<div class="actionStatus" ng-show="active">'
            +   '<div class="success" ng-show="status === true">{{successText}}</div>'
            +   '<div class="success" ng-show="status === false">{{failText}}</div>'
            +   '<div class="success" ng-show="status === null"><div class="progress small"></div> {{loadingText}}</div>'
            + '</div>'
  };
});
