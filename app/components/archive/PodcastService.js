'use strict';

angular.module('snotes30App')
.service('PodcastService', function ($rootScope, $q, Restangular) {
  var podcasts = Restangular.all('podcasts');

  this.getBySlug = function (slug) {
    return podcasts.get(slug);
  };
});
