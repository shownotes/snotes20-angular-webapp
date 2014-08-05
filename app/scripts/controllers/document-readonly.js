'use strict';

angular.module('snotes30App')
  .controller('DocumentReadonlyCtrl', function ($scope, $rootScope, $sce, $interval, docname, doc, DocumentService) {
    $scope.doc = doc;
    $scope.episode = doc.episode;

    $scope.format = "htmllist";
    $scope.formats = [
      { name: 'htmllist', type: 'html', caption: 'Liste' },
      { name: 'html', type: 'html', caption: 'Block' },
      { name: 'osf', type: 'osf', caption: 'OSF' },
      { name: 'md', type: 'plain', caption: 'Markdown' },
      { name: 'reaper', type: 'plain', caption: 'Reaper' },
      { name: 'audacity', type: 'plain', caption: 'Audacity' },
      { name: 'chapter', type: 'plain', caption: 'Kapitel' },
      { name: 'raw', type: 'plain', caption: 'Original' }
    ];

    $scope.enableFormat = function (format) {
      $scope.format = format;
    };

    $scope.download = function () {
      var hiddenElement = document.createElement('a');
      hiddenElement.href = 'data:attachment,' + encodeURI($scope.content.osf);
      hiddenElement.target = '_blank';
      hiddenElement.download = "shownotes_" + doc.name + ".txt";
      hiddenElement.click();
    };

    $scope.content = {};

    function updateText() {
      var type = 'osf';

      if($scope.format.name == 'raw')
        type = 'raw';

      DocumentService.getText(docname, type, false).then(function (resp) {
        $scope.content[type] = resp[type];
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
