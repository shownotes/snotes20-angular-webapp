'use strict';

angular.module('snotes30App')
.service('DocumentService', function ($rootScope, $q, Restangular) {
  var documents = Restangular.all('documents');
  var editorCache = null;

  this.getByName = function (name) {
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
  };

  this.getEditor = function (name) {
    var deferred = $q.defer();

    if(editorCache === null) {
      Restangular.all('editors').getList().then(function (editors) {
        editorCache = {};

        for (var i = 0; i < editors.length; i++) {
          editorCache[editors[i].short] = editors[i];
        }

        deferred.resolve(editorCache[name]);
      });
    } else {
      deferred.resolve(editorCache[name]);
    }

    return deferred.promise;
  }
});
