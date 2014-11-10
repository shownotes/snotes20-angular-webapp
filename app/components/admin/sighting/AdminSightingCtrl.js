'use strict';

angular.module('snotes30App')
  .controller('AdminSightingCtrl', function ($scope, todos, DocumentService) {
    $scope.todos = todos.data;
    $scope.count = todos.count;

    $scope.$watch('search', function (key) {
      DocumentService.getTodo(key).then(function (todos) {
        $scope.todos = todos.data;
      });
    });
  });
