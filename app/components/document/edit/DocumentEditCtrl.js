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
      return $scope.doc.meta.shownoters.indexOf($rootScope.currentUser.username) !== -1;
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
    })
});
