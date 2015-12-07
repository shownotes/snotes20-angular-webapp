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
    'angucomplete-alt',
    'restangular',
    'pascalprecht.translate'
  ])
  .config(function ($stateProvider, $urlRouterProvider, $locationProvider, $httpProvider, RestangularProvider, CONFIG, $translateProvider) {

    function getDocResolvers (edit) {
      return {
        'doc': ['DocumentService', '$stateParams', function (DocumentService, $stateParams) {
          return DocumentService.getByName($stateParams.name, edit);
        }]
      };
    }

    function getSighResolvers() {
      var res = getDocResolvers(false);

      res['covers'] = ['PodcastService', 'doc', function (PodcastService, doc) {
        return PodcastService.getCovers(doc.episode.podcast);
      }];

      return res;
    }

    function getEpResolvers (edit) {
      return {
        'doc': ['DocumentService', '$stateParams', function (DocumentService, $stateParams) {
          var podcast = $stateParams.podcast;
          var number = $stateParams.number;

          return DocumentService.getByEpisode(podcast, number, edit);
        }]
      };
    }

    $urlRouterProvider.otherwise("/404/");

    $stateProvider
      .state('livelist', {
        url: '/',
        templateUrl: 'components/livelist/livelist.html',
        controller: 'LiveListCtrl',
        resolve: {
          'episodes': ['Restangular', function (Restangular) {
            return Restangular.all('soonepisodes').getList();
          }]
        }
      })
      .state('document-edit', {
        url: '/doc/:name/edit/',
        templateUrl: 'components/document/edit/document-edit.html',
        controller: 'DocumentEditCtrl',
        resolve: getDocResolvers(true)
      })
      .state('document-sighting', {
        url: '/doc/:name/sigh/',
        templateUrl: 'components/document/sighting/document-sighting.html',
        controller: 'DocumentSightingCtrl',
        resolve: getSighResolvers()
      })
      .state('document-readonly', {
        url: '/doc/:name/',
        templateUrl: 'components/document/readonly/document-readonly.html',
        controller: 'DocumentReadonlyCtrl',
        resolve: getDocResolvers(false)
      })
      .state('document-readonly-pub', {
        url: '/doc/:name/:pub/',
        templateUrl: 'components/document/readonly/document-readonly.html',
        controller: 'DocumentReadonlyCtrl',
        resolve: getDocResolvers(false)
      })
      .state('admin-board', {
        url: '/admin/',
        templateUrl: 'components/admin/board/board.html'
      })
      .state('admin-sighting', {
        url: '/admin/sigh/',
        controller: 'AdminSightingCtrl',
        resolve: {
          todos: ['DocumentService', function (DocumentService) {
            return DocumentService.getTodo();
          }]
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
        templateUrl: 'components/archive/archive/archive.html',
        controller: 'ArchiveCtrl',
        resolve: {
          'recentpodcasts': ['ArchiveService', function (ArchiveService) {
            return ArchiveService.getRecentList();
          }],
          'podcasts': ['ArchiveService', function (ArchiveService) {
            return ArchiveService.getList();
          }]
        }
      })
      .state('archive-search', {
        url: '/archive/search/?q',
        templateUrl: 'components/archive/search/search.html',
        controller: 'ArchiveSearchCtrl'
      })
      .state('statistics', {
        url: '/statistics/',
        templateUrl: 'components/statistics/statistics.html',
        controller: 'StatisticsCtrl'
      })
      .state('faq', {
        url: '/faq/',
        templateUrl: 'components/static/faq.html'
      })
      .state('wandler', {
        url: '/wandler/',
        templateUrl: 'components/static/wandler.html'
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
      .state('archive-podcast', {
        url: '/:podcast/',
        templateUrl: 'components/archive/podcast/podcast.html',
        resolve: {
          'podcast': ['PodcastService', '$stateParams', function (PodcastService, $stateParams) {
            return PodcastService.getBySlug($stateParams.podcast);
          }]
        },
        controller: 'ArchivePodcastCtrl'
      })
      .state('view-episode', {
        url: '/:podcast/:number/',
        templateUrl: 'components/document/readonly/document-readonly.html',
        controller: 'DocumentReadonlyCtrl',
        resolve: getEpResolvers(false)
      })
      .state('edit-episode', {
        url: '/:podcast/:number/edit/',
        templateUrl: 'components/document/edit/document-edit.html',
        controller: 'DocumentEditCtrl',
        resolve: getEpResolvers(true)
      })
      .state('view-episode-pub', {
        url: '/:podcast/:number/:pub/',
        templateUrl: 'components/document/readonly/document-readonly.html',
        controller: 'DocumentReadonlyCtrl',
        resolve: getEpResolvers(false)
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
      // http://stackoverflow.com/a/25688395/2486196
      $httpProvider.interceptors.push(function($q, $timeout) {
        return {
          'response': function(response) {
            var defer = $q.defer();
            $timeout(function() {
              defer.resolve(response);
            }, 2300);
            return defer.promise;
          }
        };
      });
    }

    //delayHttp();

    //i18n
    $translateProvider
      .useStaticFilesLoader({
        prefix: 'languages/lang_',
        suffix: '.json'
      })
      .preferredLanguage('de_DE');

  })
  .run(function ($cookies, Restangular) {
    Restangular.addFullRequestInterceptor(function(element, operation, what, url, headers, query) {
      headers['X-CSRFToken'] = $cookies.csrftoken;
    });
  })
  .run(function ($rootScope, $state) {
    $rootScope.$on("$stateChangeError", function(event, toState, toParams, fromState, fromParams, error) {
      if(error.status === 403) {
        if(toState.name == "document-edit") {
          $state.go("document-readonly", toParams);
          return;
        }
      }

      if(error.status === 404 || error.status === 403) {
        $state.go(error.status + "");
      } else {
        console.log(error);
      }
    });

    var loadingTimeouts = [];

    $rootScope.$on('$stateChangeStart', function(event, toState, toParams, fromState, fromParams) {
      loadingTimeouts.push(setTimeout(function () {
        angular.element(".cccontent").addClass("ng-hide");
        angular.element("section.navigation_loading").removeClass("ng-hide");
      }, 200));
    });

    $rootScope.$on('$stateChangeSuccess', function(event, toState, toParams, fromState, fromParams) {
      while(loadingTimeouts.length > 0) clearTimeout(loadingTimeouts.pop());

      angular.element(".cccontent").removeClass("ng-hide");
      angular.element("section.navigation_loading").addClass("ng-hide");
    });
  })
  .value('cgBusyDefaults',{
    message:'Doing magic!',
    backdrop: true,
    templateUrl: 'components/shared/loading.html',
    delay: 200,
    minDuration: 50
  });
