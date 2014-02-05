'use strict';

angular.module('snotes20App', ['ngRoute']);

angular.module('snotes20App').config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/', {
        templateUrl: 'views/main.html',
      //  controller: 'PhoneListCtrl'
      }).
      when('/about', {
        templateUrl: 'views/about.html',
      //  controller: 'PhoneDetailCtrl'
      }).
      otherwise({
        redirectTo: '/'
      });
  }]);