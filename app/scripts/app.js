'use strict';

angular.module('snotes20App', ['ngRoute']);

angular.module('snotes20App').config(['$routeProvider', '$locationProvider',
  function($routeProvider, $locationProvider) {
    $locationProvider.html5Mode(true);
    $routeProvider.
      when('/', {
        templateUrl: 'views/main.html',
        controller: 'MainController'
      }).
      when('/about', {
        templateUrl: 'views/about.html',
      //  controller: 'PhoneDetailCtrl'
      }).
      otherwise({
        redirectTo: '/'
      });
  }]);