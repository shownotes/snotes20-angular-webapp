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

  this.getText = function (name, type, download, pub) {
    var params = { 'type': type, 'download': download };
    if(pub !== undefined && pub.length > 0) {
      params.pub = pub;
    }
    return documents.customPOST(null, name + '/text', params);
  };

  this.createFromEpisode = function (episode) {
    return documents.post({ episode: episode.id }, { type: 'fromepisode' });
  };

  this.addPodcaster = function (doc, podcaster) {
    return doc.customPOST(podcaster, doc.name + '/podcasters');
  };

  this.delPodcaster = function (doc, podcaster) {
    return doc.customOperation('remove', doc.name + '/podcasters', null, null, podcaster);
  };

  this.addShownoter = function (doc, shownoter) {
    return doc.customPOST(shownoter, doc.name + '/shownoters');
  };

  this.delShownoter = function (doc, shownoter) {
    return doc.customOperation('remove', doc.name + '/shownoters', null, null, shownoter);
  };

  this.publish = function (doc, publication) {
    return doc.customPOST(publication, doc.name + '/publications');
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
