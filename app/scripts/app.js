'use strict';

angular.module('snotes20App', ['ngRoute', 'ngCookies', 'pascalprecht.translate']);

/**
 * A promise object provided by angular.
 * @external Promise
 * @see {@link http://docs.angularjs.org/api/ng.$q}
 */

angular.module('snotes20App').config(
	function ($routeProvider, $locationProvider, $translateProvider) {
		$translateProvider.useStaticFilesLoader({
			prefix: 'l10n/locale-',
			suffix: '.json'
		});
		$translateProvider.preferredLanguage('de');

		$locationProvider.html5Mode(true);

		$routeProvider.
			when('/', {
				templateUrl: 'views/main.html',
				controller: 'MainController'
			}).
			when('/archive', {
				templateUrl: 'views/archive.html'
			}).
			when('/about', {
				templateUrl: 'views/about.html'
			}).
			when('/help', {
				templateUrl: 'views/help.html'
			}).
			when('/contact', {
				templateUrl: 'views/contact.html'
			}).
			otherwise({
				redirectTo: '/'
			});
	});

angular.module('snotes20App')
	.run(function ($rootScope, LoginService) {
		LoginService.checkLogin().then(
			function (user) {
				$rootScope.user = user;
			},
			function () {
				$rootScope.user = null;
			}
		);
	});
