'use strict';

angular.module('snotes30App')
  .directive('documentEditor', function() {
    return {
      restrict: 'E',
      replace: true,
      scope: {
        document: '='
      },
      template: '<iframe ng-if="docurl" src="{{docurl}}"></iframe>',
      controller: function ($scope, $sce, DocumentService) {
        DocumentService.getEditor($scope.document.editor).then(function (editor) {
          $scope.docurl = $sce.trustAsResourceUrl(editor.url + '/' + $scope.document.urlname);
        });
      }
    };
  });
