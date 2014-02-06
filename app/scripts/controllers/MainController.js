'use strict';

angular.module('snotes20App')
  .controller('MainController', function ($scope) {
    $scope.pads = [
      {
        time: new Date(),
        podcast: "Einschlafen",
        name: "einschlafen-123",
        exists: false
      },

      {
        time: new Date(),
        podcast: "Einschlafen",
        name: "einschlafen-123",
        exists: true
      }
    ];

    $scope.loadMorePads = function () {
      for (var i = 0; i < 5; i++) {

        $scope.pads.push({
          time: new Date(),
          podcast: "Einschlafen",
          name: "einschlafen-" + ~~(Math.random() * 100),
          exists: true
        });
      }
    };
  });
