'use strict';

angular.module('snotes30App')
  .service('StatisticsService', function ($rootScope, Restangular) {
    var statistic = Restangular.all('statistic');

    this.getWordList = function () {
      return statistic.one("wordlist").get({top: "200"});
    };

    this.getPodcastWordList = function (slug) {
      return statistic.one("wordlist", "podcast", slug).get({top: "20"});
    };

    this.getWordListFreq = function () {
      return statistic.one("wordfrequency").get({top: "200"});
    };

    this.getPodcastWordListFreq = function (slug) {
      return statistic.one("significantwords").one("podcast", slug).get({top: "20"});
    }
  });
