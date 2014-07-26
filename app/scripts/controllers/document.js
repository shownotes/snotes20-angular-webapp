'use strict';

angular.module('snotes30App')
  .controller('DocumentCtrl', function ($scope, $rootScope, $routeParams, $sce, document, docname, DocumentService) {
    $scope.doc = document;

    function updateDocument() {
      return DocumentService.getByName(docname).then(function (doc) {
        $scope.doc = doc;
      });
    }

    DocumentService.getEditor($scope.doc.editor).then(function (editor) {
      $scope.editor = editor;
      $scope.docurl = $sce.trustAsResourceUrl(editor.url + '/' + $scope.doc.urlname);
    });

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
      $scope.doc.customPOST($scope.newpodcaster, $scope.doc.name + '/podcasters').then(function () { $scope.newpodcaster = null; }).then(updateDocument);
    };
});
