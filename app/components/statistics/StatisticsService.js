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

    this.getPodcastTimeline = function () {
      return statistic.one("timeline").one("podcast").get();
    }

    this.getEpisodeTimeline = function (slug) {
      return statistic.one("timeline").one("episode", slug).get();
    }

    this.getPodcasts = function (period) {
      var podcasts = statistic.one("podcast");
      
      if (typeof period != 'undefined') {
        var param = {};
	param.period = period;
	return podcasts.get(param);
      }
      else {
	return podcasts.get();      
      }
    }

    this.getEpisodes = function (slug, period) {
      var episodes = statistic.one("episode");
 
      if (typeof period != 'undefined') {
          var param = {};
          param.period = period;
          return episodes.one(slug).get(param);
      }
      else {
        return episodes.one(slug).get();
      }
    }      
});
