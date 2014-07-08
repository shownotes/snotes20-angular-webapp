'use strict';

/**
 * @ngdoc overview
 * @name snotes30App
 * @description
 * # snotes30App
 *
 * Main module of the application.
 */
angular
  .module('snotes30App', [
    'ngAnimate',
    'ngCookies',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'angularSpectrumColorpicker',
    'restangular'
  ])
  .config(function ($routeProvider, $locationProvider, RestangularProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/livelist.html',
        controller: 'LiveListCtrl'
      })
      .when('/doc/:name', {
        templateUrl: 'views/document.html',
        controller: 'DocumentCtrl'
      })
      .when('/rules', {
        templateUrl: 'views/rules.html'
      })
      .when('/styleguide', {
        templateUrl: 'views/styleguide.html'
      })
      .when('/user/profile', {
        templateUrl: 'views/user/profile.html',
        controller: 'UserProfileCtrl'
      })
      .when('/profile/:username', {
        templateUrl: 'views/profile.html',
        controller: 'ProfileCtrl'
      })
      .when('/user/upgrade', {
        templateUrl: 'views/user/upgrade.html',
        controller: 'UserUpgradeCtrl'
      })
      .when('/user/registration', {
        templateUrl: 'views/user/regcomplete.html'
      })
      .when('/user/activate/:token', {
        templateUrl: 'views/user/activate.html',
        controller: 'UserActivateCtrl'
      })
      .otherwise({
        templateUrl: '404.html'
      });

    $locationProvider.html5Mode(true);

    RestangularProvider.setBaseUrl('http://snotes20.com:8000/');
    RestangularProvider.setRequestSuffix('/');
    RestangularProvider.setDefaultHttpFields({
      withCredentials: true
    });

    RestangularProvider.addElementTransformer('soonepisodes', false, function(element) {
      element.create_date = Date(element.create_date);
      element.date = Date(element.date);
      element.podcast.create_date = Date(element.podcast.create_date);
      element.document.create_date = Date(element.document.create_date);
      return element;
    });
  })
  .run(function ($cookies, Restangular) {
    Restangular.addFullRequestInterceptor(function(element, operation, what, url, headers, query) {
      headers['X-CSRFToken'] = $cookies.csrftoken;
    });
  });
