'use strict';

angular.module('snotes30App')
  .controller('DocumentEditCtrl', function ($scope, $rootScope, $sce, $state, $interval, doc, DocumentService, docEditChatSocket) {
    $scope.doc = doc;
    $scope.canPublish = false;

    function updateDocument() {
      return DocumentService.getByName(doc.name).then(function (doc) {
        $scope.doc = doc;
      });
    }

    $scope.doc.customGET($scope.doc.name + '/canpublish').then(function () {
      $scope.canPublish = true;
    }, angular.noop);

    $scope.isShownoter = function () {
      for (var i = 0; i < $scope.doc.meta.shownoters.length; i++) {
        var snoter = $scope.doc.meta.shownoters[i];
        if(snoter.name == $rootScope.currentUser.username) {
          return true;
        }
      }
      return false;
    };

    $scope.addShownoter = function () {
      $scope.doc.customPOST({}, $scope.doc.name + '/contributed').then(updateDocument);
    };

    $scope.delShownoter = function () {
      $scope.doc.customDELETE($scope.doc.name + '/contributed').then(updateDocument);
    };

    $scope.addPodcaster = function (podcaster) {
      return DocumentService.addPodcaster(doc, podcaster).then(updateDocument);
    };

    $scope.delPodcaster = function (podcaster) {
      return DocumentService.delPodcaster(doc, podcaster).then(updateDocument);
    };

    $scope.sendChatMsg = function () {
      $scope.doc.customPOST($scope.chatmsg, $scope.doc.name + '/chat').then(function () { $scope.chatmsg = null; });
    };

    $scope.doSighting = function () {
      $state.go('document-sighting', { name: $scope.doc.name });
    };

    $scope.requestSighting = function () {
      $scope.doc.customPOST({}, $scope.doc.name + '/publicationrequests').then(updateDocument);
    };

    $scope.hasPublications = function () {
      var episode = $scope.doc.episode;
      return episode && episode.publications.length > 0;
    };

    $scope.hasPublicationRequests = function () {
      var episode = $scope.doc.episode;
      return episode && episode.publicationrequests.length > 0;
    };

    function getChatMsgs(since) {
      var params = {};
      if(since) {
        params['since'] = since;
      }
      $scope.doc.customGET($scope.doc.name + '/chat', params).then(function (msgs) {
        if(since) {
          $scope.chatmessages = $scope.chatmessages.concat(msgs);
        } else {
          $scope.chatmessages = msgs;
        }
      });
    }

    getChatMsgs();

    docEditChatSocket.emit('JOIN_DOC', doc.name);

    docEditChatSocket.on('DOCUMENT_CHATMESSAGE', function (msg) {
        $scope.chatmessages.push(msg);
    });

    var heightUpdateInt = $interval(function () {
      var bodyHeight = angular.element(window).height();
      var $editor = angular.element('.editor');
      var offset = Math.ceil($editor.offset()['top']) + 3;
      $editor.css('height', bodyHeight - offset);
    }, 50);

    $scope.$on('$destroy', function () {
      $interval.cancel(heightUpdateInt);
    });
});
