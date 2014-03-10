'use strict';

// based on http://stackoverflow.com/a/12631074/2486196
angular.module('snotes20App').
	directive('activeLink', ['$location', function (location) {
		return {
			restrict: 'A',
			link: function (scope, element, attrs) {
				var clazz = attrs.activeLink;
				scope.location = location;
				scope.$watch('location.path()', function (newPath) {
					if (attrs.ngHref === newPath) {
						element.addClass(clazz);
					} else {
						element.removeClass(clazz);
					}
				});
			}
		};
	}]);