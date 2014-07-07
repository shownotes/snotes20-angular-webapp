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
      .when('/styleguide', {
        templateUrl: 'views/styleguide.html'
      })
      .when('/user/profile', {
        templateUrl: 'views/user/profile.html',
        controller: 'UserProfileCtrl'
      })
      .when('/profile/:user', {
        templateUrl: 'views/profile.html',
      })
      .when('/user/upgrade', {
        templateUrl: 'views/user/upgrade.html',
        controller: 'UserUpgradeCtrl'
      })
      .when('/user/activate', {
        templateUrl: 'views/user/activate.html',
        controller: 'UserActivateCtrl'
      })
      .otherwise({
        redirectTo: '/'
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
