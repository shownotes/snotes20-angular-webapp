'use strict';

angular.module('snotes30App')
.service('PodcastService', function ($rootScope, $q, Restangular) {
  var podcasts = Restangular.all('podcasts');

  this.getBySlug = function (slug) {
    return podcasts.get(slug);
  };

  this.getCovers = function (podcast) {
    return podcasts.customGET((podcast.slug || podcast) + '/covers');
  };

  this.getNumbers = function (podcast) {
    return podcasts.customGET((podcast.slug || podcast) + '/numbers');
  };
});
