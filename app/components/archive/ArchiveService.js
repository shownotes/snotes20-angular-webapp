'use strict';

angular.module('snotes30App')
.service('ArchiveService', function ($rootScope, $q, Restangular) {
  var archive = Restangular.all('archive');

  this.getList = function () {
    return archive.getList()

  this.getFullList = function () {
    return archive.getList({type: 'full'});
  };

  this.getRecentList = function () {
    return archive.getList({type: 'recent'});
  };

  this.search = function (words) {
    return archive.customPOST({words: words}, 'search');
  }
});
