'use strict';

angular.module('snotes30App')
  .controller('DocumentReadonlyCtrl', function ($scope, $rootScope, $sce, $interval, docname, document, DocumentService) {
    $scope.document = document;
    $scope.episode = document.episode;

    $scope.format = "htmllist";
    $scope.formats = [
      { name: 'htmllist', caption: 'Liste' },
      { name: 'html', caption: 'Block' },
      { name: 'osf', caption: 'OSF' },
      { name: 'md', caption: 'Markdown' },
      { name: 'reaper', caption: 'Reaper' },
      { name: 'audacity', caption: 'Audacity' },
      { name: 'chapter', caption: 'Kaptiel' }
    ];

    $scope.enableFormat = function (format) {
      $scope.format = format;
    };

    function updateText() {
      DocumentService.getText(docname).then(function (resp) {
        var text = resp.text;
        $scope.rawText = text;
      })
    }

    updateText();

    var textUpdateInt = $interval(function () {
      updateText();
    }, 500);

    $scope.$on('$destroy', function () {
      $interval.cancel(textUpdateInt);
    });
});
