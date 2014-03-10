'use strict';

angular.module('snotes20App').directive('focusOn', function () {
	return {
		restrict: 'A',
		link: function (scope, element, attr) {
			scope.$watch(attr.focusOn, function (e) {
				if (scope[attr.focusOn]) {
					element[0].focus();
				}
			});
		}
	};
});