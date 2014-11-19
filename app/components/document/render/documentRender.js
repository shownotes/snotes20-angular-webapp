'use strict';

angular.module('snotes30App')
  .directive('documentRender', function() {
    return {
      restrict: 'E',
      replace: true,
      scope: {
        document: '=',
        showFormats: '@',
        publication: '=?',
        refresh: '=?',
        formatName: '=?'
      },
      templateUrl: '/components/document/render/document-render.html',
      controller: function ($scope, $interval, DocumentService) {
        $scope.formats = [
          { name: 'list',     type: 'html',  caption: 'Liste' },
          { name: 'block',    type: 'html',  caption: 'Block' },
          { name: 'md',       type: 'plain', caption: 'Markdown' },
          { name: 'reaper',   type: 'plain', caption: 'Reaper' },
          { name: 'audacity', type: 'plain', caption: 'Audacity' },
          { name: 'chapter',  type: 'plain', caption: 'Kapitel' },
          { name: 'raw',      type: 'plain', caption: 'Original' },
          { name: 'osf',      type: 'plain', caption: 'OSF' }
        ];

        if (!$scope.formatName) {
          $scope.formatName = $scope.formats[0].name;
        }

        $scope.format = function () {
          for (var i = 0; i < $scope.formats.length; i++) {
            if($scope.formats[i].name == $scope.formatName)
              return $scope.formats[i];
          }
          return null;
        };

        $scope.enableFormat = function (format) {
          $scope.formatName = format;
          updateText();
        };

        $scope.download = function () {
          var hiddenElement = document.createElement('a');
          hiddenElement.href = 'data:attachment,' + encodeURI($scope.content.osf);
          hiddenElement.target = '_blank';
          hiddenElement.download = "shownotes_" + doc.name + ".txt";
          hiddenElement.click();
        };

        $scope.content = "";

        var nunjucksenv = new nunjucks.Environment();

        // http://stackoverflow.com/a/10073788
        function pad(n, width, z) {
          z = z || '0';
          n = n + '';
          return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
        }

        nunjucksenv.addFilter('htime', function(time, ms) {
          var milliseconds = pad(time % 1000, 4);
          time = time / 1000;
          var seconds = pad(time % 60, 2);
          var minutes = pad(Math.floor((time / 60) % 60), 2);
          var hours = pad(Math.floor((time / 60 / 60) % 60), 2);

          var str =  hours + ":" + minutes + ":" + seconds;
          if(ms) str += "." + milliseconds;
          return str;
        });

        function updateText() {
          var type = null;

          switch($scope.formatName) {
            case 'raw': type = 'raw';  break;
            default:    type = 'json'; break;
          }

          DocumentService.getText($scope.document.name, type, false, $scope.publication).then(function (resp) {
            var data = resp.data;

            if(type == 'json') {
              data = nunjucksenv.render("osf_" + $scope.formatName, data);
            }

            $scope.content = data;
          })
        }

        updateText();

        if($scope.refresh !== false) {
          var textUpdateInt = $interval(function () {
            updateText();
          }, 1500);

          $scope.$on('$destroy', function () {
            $interval.cancel(textUpdateInt);
          });
        }
      }
    };
  });
