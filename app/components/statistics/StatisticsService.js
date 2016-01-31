'use strict';

angular.module('snotes30App')
  .service('StatisticsService', function ($rootScope, Restangular) {
    var statistic = Restangular.all('statistic');

    this.getWordList = function () {
      return statistic.get("wordlist", "?=200");
    };

    this.getPodcastWordList = function (slug) {
      return statistic.get("wordlist", "podcast", slug, "?=20");
    };

    this.getWordListFreq = function () {
      return statistic.get("wordfrequency", "?=100");
    };

    this.getPodcastWordListFreq = function (slug) {
      return statistic.get("wordfrequency", slug + "/?top=20");
    }
  });
