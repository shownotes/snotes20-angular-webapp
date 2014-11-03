'use strict';

angular.module('snotes30App')
  .controller('DocumentReadonlyCtrl', function ($scope, $rootScope, $sce, $interval, docname, doc, DocumentService) {
    $scope.doc = doc;
    $scope.episode = doc.episode;

    $scope.formats = [
      { name: 'list',     type: 'html',  caption: 'Liste' },
      { name: 'block',    type: 'html',  caption: 'Block' },
      { name: 'md',       type: 'plain', caption: 'Markdown' },
      { name: 'reaper',   type: 'plain', caption: 'Reaper' },
      { name: 'audacity', type: 'plain', caption: 'Audacity' },
      { name: 'chapter',  type: 'plain', caption: 'Kapitel' },
      { name: 'raw',      type: 'plain', caption: 'Original' },
      { name: 'osf',      type: 'osf',   caption: 'OSF' }
    ];

    $scope.format = $scope.formats[0];

    $scope.enableFormat = function (format) {
      $scope.format = format;
      updateText();
    };

    $scope.download = function () {
      var hiddenElement = document.createElement('a');
      hiddenElement.href = 'data:attachment,' + encodeURI($scope.content.osf);
      hiddenElement.target = '_blank';
      hiddenElement.download = "shownotes_" + doc.name + ".txt";
      hiddenElement.click();
    };

    $scope.content = {};

    var nunjucksenv = new nunjucks.Environment();

    // http://stackoverflow.com/a/10073788
    function pad(n, width, z) {
      z = z || '0';
      n = n + '';
      return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
    }

    nunjucksenv.addFilter('htime', function(time) {
      var milliseconds = time % 1000;
      time = time / 1000;
      var seconds = pad(time % 60, 2);
      var minutes = pad(Math.floor((time / 60) % 60), 2);
      var hours = pad(Math.floor((time / 60 / 60) % 60), 2);

      return hours + ":" + minutes + ":" + seconds;
    });

    function updateText() {
      var type = null;

      switch($scope.format.name) {
        case 'raw': type = 'raw';  break;
        case 'osf': type = 'osf';  break;
        default:    type = 'json'; break;
      }

      DocumentService.getText(docname, type, false).then(function (resp) {
        var data = resp.data;

        if(type == 'json') {
          data = nunjucksenv.render("osf_" + $scope.format.name, data);
        }

        $scope.content = data;
      })
    }

    updateText();

    var textUpdateInt = $interval(function () {
      updateText();
    }, 1500);

    $scope.$on('$destroy', function () {
      $interval.cancel(textUpdateInt);
    });
});
