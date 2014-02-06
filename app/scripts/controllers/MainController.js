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
  });
