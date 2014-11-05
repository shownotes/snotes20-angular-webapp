'use strict';

angular.module('snotes30App')
  .directive('documentEditor', function() {
    return {
      restrict: 'E',
      replace: true,
      scope: {
        document: '='
      },
      template: '<iframe src="{{docurl}}"></iframe>',
      controller: function ($scope, $sce, DocumentService) {
        DocumentService.getEditor($scope.document.editor).then(function (editor) {
          console.log("fooo");
          $scope.docurl = $sce.trustAsResourceUrl(editor.url + '/' + $scope.document.urlname);
        });
      }
    };
  });
