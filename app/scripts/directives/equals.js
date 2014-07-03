'use strict';

// http://stackoverflow.com/a/18014975/2486196
angular.module('snotes30App').directive('equals', function() {
  return {
    restrict: 'A', // only activate on element attribute
    require: '?ngModel', // get a hold of NgModelController
    link: function(scope, elem, attrs, ngModel) {
      if(!ngModel) return; // do nothing if no ng-model

      var visible = true;

      // watch own value and re-validate on change
      scope.$watch(attrs.ngModel, function() {
        validate();
      });

      // observe the other value and re-validate on change
      attrs.$observe('equals', function (val) {
        validate();
      });

      if(attrs.ngShow) {
        scope.$watch(attrs.ngShow, function () {
          visible = scope.$eval(attrs.ngShow);
          validate();
        });
      }

      var validate = function() {
        // values
        var val1 = ngModel.$viewValue;
        var val2 = attrs.equals;

        // set validity
        ngModel.$setValidity('equals', val1 === val2 || !visible);
      };
    }
  }
});
