'use strict';

angular.module('snotes30App')
  .controller('DocumentCtrl', function ($scope, $routeParams, $sce, DocumentService, AuthenticationService) {
    var name = $routeParams.name;
    var me = null;

    function updateDocument() {
      return DocumentService.getByName(name).then(function (doc) {
        $scope.doc = doc;
      }, function () {
        alert('gibts nicht');
      });
    }

    updateDocument().then(function () {
      DocumentService.getEditor($scope.doc.editor).then(function (editor) {
        $scope.editor = editor;
        $scope.docurl = $sce.trustAsResourceUrl(editor.url + '/' + $scope.doc.urlname);
      });
    });

    AuthenticationService.getStatus().then(function (status) { me = status.user; });

    $scope.isShownoter = function () {
      if(!$scope.doc)
        return false;
      return $scope.doc.meta.shownoters.indexOf(me.username) !== -1;
    };

    $scope.addShownoter = function () {
      $scope.doc.customPOST({}, $scope.doc.name + '/contributed').then(updateDocument);
    };

    $scope.delShownoter = function () {
      $scope.doc.customDELETE($scope.doc.name + '/contributed').then(updateDocument);
    };
});
