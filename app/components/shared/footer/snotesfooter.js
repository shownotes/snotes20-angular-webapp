'use strict';

angular.module('snotes30App')
.directive('snotesFooter', function() {
  return {
    restrict: 'E',
    replace: true,
    templateUrl: 'components/shared/footer/footer.html',
  };
});
