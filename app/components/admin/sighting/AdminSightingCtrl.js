'use strict';

angular.module('snotes30App')
  .controller('AdminSightingCtrl', function ($scope, todos, DocumentService) {
    $scope.todos = todos.data;
    $scope.count = todos.count;
  });
