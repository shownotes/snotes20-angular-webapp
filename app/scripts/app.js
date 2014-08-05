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
    'cgBusy',
    'restangular'
  ])
  .config(function ($routeProvider, $locationProvider, $httpProvider, RestangularProvider) {
    var docResvolers = {
      'doc': ['DocumentService', '$route', function (DocumentService, $route) {
        return DocumentService.getByName($route.current.params.name);
      }],
      'docname': ['$route', function ($route) {
        return $route.current.params.name;
      }]
    };

    $routeProvider
      .when('/', {
        templateUrl: 'views/livelist.html',
        controller: 'LiveListCtrl'
      })
      .when('/doc/:name', {
        templateUrl: 'views/document.html',
        controller: 'DocumentCtrl',
        resolve: docResvolers
      })
      .when('/doc/:name/readonly', {
        templateUrl: 'views/document-readonly.html',
        controller: 'DocumentReadonlyCtrl',
        resolve: docResvolers
      })
      .when('/sighting', {
        templateUrl: 'views/sighting.html'
      })
      .when('/rules', {
        templateUrl: 'views/rules.html'
      })
      .when('/imprint', {
        templateUrl: 'views/imprint.html'
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
      .when('/user/pwreset/:username/:token', {
        templateUrl: 'views/user/pwreset.html',
        controller: 'UserPwResetCtrl'
      })
      .when('/user/activate/:username/:token', {
        templateUrl: 'views/user/activate.html',
        controller: 'UserActivateCtrl'
      })
      .when('/user/confirm/:username/:token', {
        templateUrl: 'views/user/activate.html',
        controller: 'UserActivateCtrl'
      })
      .when('/admin/importstatus', {
        templateUrl: 'views/admin/importstatus.html',
        controller: 'ImportStatusCtrl'
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
      element.create_date = new Date(element.create_date);
      element.date = new Date(element.date);
      element.podcast.create_date = new Date(element.podcast.create_date);
      if(element.document)
        element.document.create_date = new Date(element.document.create_date);
      return element;
    });

    RestangularProvider.addElementTransformer('importerlogs', false, function(element) {
      function patchTimeAttrs(obj) {
        obj.starttime = new Date(obj.starttime);
        obj.endtime = new Date(obj.endtime);
      }

      patchTimeAttrs(element);

      for(var i = 0; i < element.sources.length; i++) {
        var source = element.sources[i];
        patchTimeAttrs(source);

        for(var j = 0; j < source.jobs.length; j++) {
          var job = source.jobs[i];
          patchTimeAttrs(job);
        }
      }

      return element;
    });

    function delayHttp() {
      $httpProvider.responseInterceptors.push(["$q", "$timeout", function ($q, $timeout) {
        return function (promise) {
          var defer = $q.defer();
          $timeout(function () { promise.then(defer.resolve, defer.reject); }, 700);
          return defer.promise;
        };
      }]);
    }

    //delayHttp();
  })
  .run(function ($cookies, Restangular) {
    Restangular.addFullRequestInterceptor(function(element, operation, what, url, headers, query) {
      headers['X-CSRFToken'] = $cookies.csrftoken;
    });
  })
  .run(function ($rootScope, $location) {
    $rootScope.$on("$routeChangeError", function(event, current, previous, rejection) {
      if(rejection.status && rejection.status == 404) {
        $location.url('/404');
      }
    });
  })
  .value('cgBusyDefaults',{
    message:'Doing magic!',
    backdrop: true,
    templateUrl: 'views/loading.html',
    delay: 200,
    minDuration: 50
  });
