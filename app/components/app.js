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
      }]
    };

    var epResolvers = {
      'doc': ['DocumentService', '$stateParams', function (DocumentService, $stateParams) {
        var podcast = $stateParams.podcast;
        var number = $stateParams.number;

        return DocumentService.getByEpisode(podcast, number);
      }]
    };

    $urlRouterProvider.otherwise("/404/");

    $stateProvider
      .state('livelist', {
        url: '/',
        templateUrl: 'components/livelist/livelist.html',
        controller: 'LiveListCtrl'
      })
      .state('document-edit', {
        url: '/doc/:name/edit/',
        templateUrl: 'components/document/edit/document-edit.html',
        controller: 'DocumentEditCtrl',
        resolve: docResvolers
      })
      .state('document-sighting', {
        url: '/doc/:name/sigh/',
        templateUrl: 'components/document/sighting/document-sighting.html',
        controller: 'DocumentSightingCtrl',
        resolve: docResvolers
      })
      .state('document-readonly', {
        url: '/doc/:name/',
        templateUrl: 'components/document/readonly/document-readonly.html',
        controller: 'DocumentReadonlyCtrl',
        resolve: docResvolers
      })
      .state('document-readonly-pub', {
        url: '/doc/:name/:pub/',
        templateUrl: 'components/document/readonly/document-readonly.html',
        controller: 'DocumentReadonlyCtrl',
        resolve: docResvolers
      })
      .state('admin-board', {
        url: '/admin/',
        templateUrl: 'components/admin/board/board.html'
      })
      .state('admin-sighting', {
        url: '/admin/sigh/',
        controller: 'AdminSightingCtrl',
        resolve: {
          todos: function (DocumentService) {
            return DocumentService.getTodo();
          }
        },
        templateUrl: 'components/admin/sighting/sighting.html'
      })
      .state('admin-importstatus', {
        url: '/admin/importstatus/',
        templateUrl: 'components/admin/importstatus/importstatus.html',
        controller: 'ImportStatusCtrl'
      })
      .state('404', {
        templateUrl: '404.html'
      })
      .state('404u', {
        url: '/404/',
        templateUrl: '404.html'
      })
      .state('403', {
        templateUrl: '403.html'
      })
      .state('archive', {
        url: '/archive/',
        templateUrl: 'components/archive/archive.html'
      })
      .state('archive-search', {
        url: '/archive/search/',
        templateUrl: 'components/archive/search.html'
      })
      .state('archive-podcast', {
        url: '/archive/podcast/',
        templateUrl: 'components/archive/podcast.html'
      })
      .state('faq', {
        url: '/faq/',
        templateUrl: 'components/static/faq.html'
      })
      .state('rules', {
        url: '/rules/',
        templateUrl: 'components/static/rules.html'
      })
      .state('community', {
        url: '/community/',
        templateUrl: 'components/static/community.html'
      })
      .state('privacy', {
        url: '/privacy/',
        templateUrl: 'components/static/privacy.html'
      })
      .state('donate', {
        url: '/donate/',
        templateUrl: 'components/static/donate.html'
      })
      .state('imprint', {
        url: '/imprint/',
        templateUrl: 'components/static/imprint.html'
      })
      .state('styleguide', {
        url: '/styleguide/',
        templateUrl: 'components/static/imprint.html'
      })
      .state('publicprofile', {
        url: '/profile/:username/',
        templateUrl: 'components/publicprofile/publicprofile.html',
        controller: 'PublicProfileCtrl'
      })
      .state('user-profile', {
        url: '/user/profile/',
        templateUrl: 'components/user/profile/profile.html',
        controller: 'UserProfileCtrl'
      })
      .state('user-upgrade', {
        url: '/user/upgrade/',
        templateUrl: 'components/user/upgrade/upgrade.html',
        controller: 'UserUpgradeCtrl'
      })
      .state('user-registration', {
        url: '/user/registration/',
        templateUrl: 'components/user/regcomplete/regcomplete.html'
      })
      .state('user-pwreset', {
        url: '/user/pwreset/:username/:token/',
        templateUrl: 'components/user/pwreset/pwreset.html',
        controller: 'UserPwResetCtrl'
      })
      .state('user-activate', {
        url: '/user/activate/:username/:token/',
        templateUrl: 'components/user/activate/activate.html',
        controller: 'UserActivateCtrl'
      })
      .state('user-confirm-email', {
        url: '/user/confirm/:username/:token/',
        templateUrl: 'components/user/activate/activate.html',
        controller: 'UserActivateCtrl'
      })
      .state('view-episode', {
        url: '/:podcast/:number/',
        templateUrl: 'components/document/readonly/document-readonly.html',
        controller: 'DocumentReadonlyCtrl',
        resolve: epResolvers
      })
      .state('edit-episode', {
        url: '/:podcast/:number/edit/',
        templateUrl: 'components/document/edit/document-edit.html',
        controller: 'DocumentEditCtrl',
        resolve: epResolvers
      })
       ;

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
  .run(function ($rootScope, $state) {
    $rootScope.$on("$stateChangeError", function(event, toState, toParams, fromState, fromParams, error) {
      if(error.status === 404 || error.status === 403) {
        $state.go(error.status + "");
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
