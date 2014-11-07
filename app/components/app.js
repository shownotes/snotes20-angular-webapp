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
    'ui.router',
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
  .config(function ($stateProvider, $urlRouterProvider, $locationProvider, $httpProvider, RestangularProvider, CONFIG) {
    var docResvolers = {
      'doc': ['DocumentService', '$stateParams', function (DocumentService, $stateParams) {
        return DocumentService.getByName($stateParams.name);
      }],
      'docname': ['$stateParams', function ($stateParams) {
        return $stateParams.name;
      }]
    };

    $urlRouterProvider.otherwise("/");

    $urlRouterProvider.rule(function ($injector, $location) {
      var path = $location.url();

      if(path === '/') {
        return;
      }

      // remove trailing slash
      if (path[path.length - 1] === '/' || path.indexOf('/?') > -1) {
        return path.substr(0, path.length - 1);
      }
    });

    $stateProvider
      .state('state1.list', {
        url: "/list",
        templateUrl: "partials/state1.list.html",
        controller: function($scope) {
          $scope.items = ["A", "List", "Of", "Items"];
        }
      })
      .state('livelist', {
        url: '/',
        templateUrl: 'components/livelist/livelist.html',
        controller: 'LiveListCtrl'
      })
      .state('document-edit', {
        url: '/doc/:name',
        templateUrl: 'components/document/edit/document-edit.html',
        controller: 'DocumentEditCtrl',
        resolve: docResvolers
      })
      .state('document-readonly', {
        url: '/doc/:name/readonly',
        templateUrl: 'components/document/readonly/document-readonly.html',
        controller: 'DocumentReadonlyCtrl',
        resolve: docResvolers
      })
      .state('document-sighting', {
        url: '/doc/:name/sigh', // /doc/bluemoon-2014-11-07-11-15-03/sigh
        templateUrl: 'components/document/sighting/document-sighting.html',
        controller: 'DocumentSightingCtrl',
        resolve: docResvolers
      })
      .state('admin-board', {
        url: '/admin',
        templateUrl: 'components/admin/board/board.html'
      })
      .state('admin-sighting', {
        url: '/admin/sigh',
        templateUrl: 'components/admin/sighting/sighting.html'
      })
      .state('admin-importstatus', {
        url: '/admin/importstatus',
        templateUrl: 'components/admin/importstatus/importstatus.html',
        controller: 'ImportStatusCtrl'
      })
      .state('archive', {
        url: '/archive',
        templateUrl: 'components/archive/archive.html'
      })
      .state('archive-search', {
        url: '/archive/search',
        templateUrl: 'components/archive/search.html'
      })
      .state('archive-podcast', {
        url: '/archive/podcast',
        templateUrl: 'components/archive/podcast.html'
      })
      .state('faq', {
        url: '/faq',
        templateUrl: 'components/static/faq.html'
      })
      .state('rules', {
        url: '/rules',
        templateUrl: 'components/static/rules.html'
      })
      .state('community', {
        url: '/community',
        templateUrl: 'components/static/community.html'
      })
      .state('donate', {
        url: '/donate',
        templateUrl: 'components/static/donate.html'
      })
      .state('imprint', {
        url: '/imprint',
        templateUrl: 'components/static/imprint.html'
      })
      .state('styleguide', {
        url: '/styleguide',
        templateUrl: 'components/static/imprint.html'
      })
      .state('publicprofile', {
        url: '/profile/:username',
        templateUrl: 'components/publicprofile/publicprofile.html',
        controller: 'PublicProfileCtrl'
      })
      .state('user-profile', {
        url: '/user/profile',
        templateUrl: 'components/user/profile/profile.html',
        controller: 'UserProfileCtrl'
      })
      .state('user-upgrade', {
        url: '/user/upgrade',
        templateUrl: 'components/user/upgrade/upgrade.html',
        controller: 'UserUpgradeCtrl'
      })
      .state('user-registration', {
        url: '/user/registration',
        templateUrl: 'components/user/regcomplete/regcomplete.html'
      })
      .state('user-pwreset', {
        url: '/user/pwreset/:username/:token',
        templateUrl: 'components/user/pwreset/pwreset.html',
        controller: 'UserPwResetCtrl'
      })
      .state('user-activate', {
        url: '/user/activate/:username/:token',
        templateUrl: 'components/user/activate/activate.html',
        controller: 'UserActivateCtrl'
      })
      .state('user-confirm-email', {
        url: '/user/confirm/:username/:token',
        templateUrl: 'components/user/activate/activate.html',
        controller: 'UserActivateCtrl'
      });

    $locationProvider.html5Mode(true);

    RestangularProvider.setBaseUrl(CONFIG.apiBaseUrl);
    RestangularProvider.setRequestSuffix('/');
    RestangularProvider.setDefaultHttpFields({
      withCredentials: true
    });

    RestangularProvider.setDefaultHeaders({'Content-Type': 'application/json'});

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
      console.log(rejection);
      /*
      if(rejection.status && rejection.status == 404) {
        $location.url('/404');
      }*/
    });
  })
  .value('cgBusyDefaults',{
    message:'Doing magic!',
    backdrop: true,
    templateUrl: 'components/shared/loading.html',
    delay: 200,
    minDuration: 50
  });
