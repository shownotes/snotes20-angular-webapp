'use strict';

angular.module('snotes20App', ['ngRoute', 'pascalprecht.translate']);

angular.module('snotes20App').config(['$routeProvider', '$locationProvider', '$translateProvider',
  function($routeProvider, $locationProvider, $translateProvider) {
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
      otherwise({
        redirectTo: '/'
      });
  }]);