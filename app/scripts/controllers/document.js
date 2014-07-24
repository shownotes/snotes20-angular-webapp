'use strict';

angular.module('snotes30App')
  .controller('DocumentCtrl', function ($scope, $routeParams, $sce, DocumentService) {
    var name = $routeParams.name;

    DocumentService.getByName(name).then(function (doc) {
      $scope.doc = doc;
      DocumentService.getEditor(doc.editor).then(function (editor) {
        $scope.editor = editor;
        $scope.docurl = $sce.trustAsResourceUrl(editor.url + '/' + doc.urlname);
      })
    }, function () {
      alert('gibts nicht');
    });
  });
