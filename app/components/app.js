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
    'btford.socket-io',
    'restangular'
  ])
  .config(function ($routeProvider, $locationProvider, $httpProvider, RestangularProvider, CONFIG) {
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
        templateUrl: 'components/livelist/livelist.html',
        controller: 'LiveListCtrl'
      })
      .when('/doc/:name', {
        templateUrl: 'components/document/edit/document-edit.html',
        controller: 'DocumentEditCtrl',
        resolve: docResvolers
      })
      .when('/doc/:name/readonly', {
        templateUrl: 'components/document/edit/document-readonly.html',
        controller: 'DocumentReadonlyCtrl',
        resolve: docResvolers
      })
      .when('/doc/:name/sigh', {
        templateUrl: 'components/document/edit/document-sighting.html',
        controller: 'DocumentSightingCtrl',
        resolve: docResvolers
      })
      .when('/admin', {
        templateUrl: 'components/admin/board/board.html'
      })
      .when('/admin/sigh', {
        templateUrl: 'components/admin/sighting/sighting.html'
      })
      .when('/admin/importstatus', {
        templateUrl: 'components/admin/importstatus/importstatus.html',
        controller: 'ImportStatusCtrl'
      })
      .when('/archive', {
        templateUrl: 'components/archive/archive.html'
      })
      .when('/archive/search', {
        templateUrl: 'components/archive/search.html'
      })
      .when('/archive/podcast', {
        templateUrl: 'components/archive/podcast.html'
      })
      .when('/faq', {
        templateUrl: 'components/static/faq.html'
      })
      .when('/rules', {
        templateUrl: 'components/static/rules.html'
      })
      .when('/community', {
        templateUrl: 'components/static/community.html'
      })
      .when('/donate', {
        templateUrl: 'components/static/donate.html'
      })
      .when('/imprint', {
        templateUrl: 'components/static/imprint.html'
      })
      .when('/styleguide', {
        templateUrl: 'components/static/imprint.html'
      })
      .when('/profile/:username', {
        templateUrl: 'components/publicprofile/publicprofile.html',
        controller: 'PublicProfileCtrl'
      })
      .when('/user/profile', {
        templateUrl: 'components/user/profile/profile.html',
        controller: 'UserProfileCtrl'
      })
      .when('/user/upgrade', {
        templateUrl: 'components/user/upgrade/upgrade.html',
        controller: 'UserUpgradeCtrl'
      })
      .when('/user/registration', {
        templateUrl: 'components/user/regcomplete/regcomplete.html'
      })
      .when('/user/pwreset/:username/:token', {
        templateUrl: 'components/user/pwreset/pwreset.html',
        controller: 'UserPwResetCtrl'
      })
      .when('/user/activate/:username/:token', {
        templateUrl: 'components/user/activate/activate.html',
        controller: 'UserActivateCtrl'
      })
      .when('/user/confirm/:username/:token', {
        templateUrl: 'components/user/activate/activate.html',
        controller: 'UserActivateCtrl'
      })
      .otherwise({
        templateUrl: '../404.html'
      });

    $locationProvider.html5Mode(true);

    RestangularProvider.setBaseUrl(CONFIG.apiBaseUrl);
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
    templateUrl: 'components/shared/loading.html',
    delay: 200,
    minDuration: 50
  });
