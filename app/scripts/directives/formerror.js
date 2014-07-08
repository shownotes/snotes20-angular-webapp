'use strict';

angular.module('snotes30App').directive('formError', function() {
  return {
    restrict: 'E',
    scope: {
      errors: '=errors'
    },
    template: '<div ng-show="errors" ng-repeat="err in errors">{{err}}</div>'
  };
});
