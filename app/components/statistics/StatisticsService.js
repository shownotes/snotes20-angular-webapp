'use strict';

angular.module('snotes30App')
.service('StatisticsService', function ($rootScope, Restangular) {
  var statistic = Restangular.all('statistic');

  this.getWordList = function () {
    return statistic.get("wordlist", "?=100");
  };

  this.getPodcastWordList = function (slug) {
    return statistic.getList("significantwords", "podcast", slug);
  };
});
