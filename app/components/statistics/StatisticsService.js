'use strict';

angular.module('snotes30App')
.service('StatisticsService', function ($rootScope, Restangular) {
  var statistic = Restangular.all('statistic');

  this.getWordList = function () {
    return statistic.get("wordlist");
  };
});
