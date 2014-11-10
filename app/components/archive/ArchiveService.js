'use strict';

angular.module('snotes30App')
.service('ArchiveService', function ($rootScope, $q, Restangular) {
  var archive = Restangular.all('archive');

  this.getList = function () {
    return archive.getList()
  };

  this.getRecentList = function () {
    return archive.getList();
  };
});
