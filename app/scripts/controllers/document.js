'use strict';

angular.module('snotes30App')
  .controller('DocumentCtrl', function ($scope, $routeParams, $sce, DocumentService) {
    var name = $routeParams.name;
    /*
    DocumentService.getByName(name).then(function (doc) {
      $scope.doc = doc;
      DocumentService.getEditor(doc.editor).then(function (editor) {
        $scope.editor = editor;
        $scope.docurl = $sce.trustAsResourceUrl(editor.url + '/' + doc.urlname);
      })
    }, function () {
      alert('gibts nicht');
    });
    */

  $scope.doc = {
    "name": "binaergewitter-2014-07-24-17-33-25",
    "editor": "EP",
    "create_date": "2014-07-24T17:33:25.535Z",
    "episode": {
      "id": "d6487c3012e048868a8b160936c373d2",
      "podcast": {
        "id": "e040e5afdeb844e792b2fb3972869b68",
        "source": "HOE",
        "source_id": 20907,
        "import_date": "2014-07-24T15:28:00.977Z",
        "creator": null,
        "title": "Bin\u00e4rgewitter",
        "description": "Ein Podcast, der sich mit dem Web, Technologie und Open Source Software auseinander setzt.",
        "url": "http://blog.binaergewitter.de",
        "stream": null,
        "chat": "http://webchat.freenode.net/?channels=binaergewitter\n",
        "type": "POD",
        "deleted": false,
        "approved": false,
        "create_date": "2014-07-24T15:28:00.977Z"
      },
      "creator": null,
      "number": null,
      "episode_url": null,
      "date": "2014-07-24T20:00:00Z",
      "canceled": false,
      "type": "POD",
      "create_date": "2014-07-24T15:29:07.036Z",
      "stream": "http://streams.xenim.de/binaergewitter.mp3.m3u",
      "document": {
        "name": "binaergewitter-2014-07-24-17-33-25",
        "editor": "EP",
        "create_date": "2014-07-24T17:33:25.535Z",
        "creator": 2,
        "meta": "24badef5aa764f8eb67e8a885e1c8175"
      }
    },
    "meta": {
      "podcasters": [
        {
          "id": "d5704d1729d04912866a4224ca014efb",
          "uri": "http://pritlove.org/",
          "name": "Tim Pritlove"
        }
      ],
      "shownoters": [
        "admin",
        "luto"
      ]
    },
    "urlname": "g.8jmHXsdnlBetW37V$binaergewitter-2014-07-24-17-33-25"
  }
});
