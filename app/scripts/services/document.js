'use strict';

angular.module('snotes30App')
.service('DocumentService', function ($rootScope, $q, Restangular) {
  var documents = Restangular.all('documents');

  this.getByname = function (name) {
    return documents.get(name);
  };

  this.getByEpisode = function (podcast, number) {
    return documents.customGET('', {
      podcast: podcast,
      number: number
    })
  };

  this.createFromEpisode = function (episode) {
    return documents.post({ episode: episode.id }, { type: 'fromepisode' });
  }
});
