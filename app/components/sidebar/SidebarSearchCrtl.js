'use strict';

angular.module('snotes30App')
  .controller('SidebarSearchCrtl', function ($scope, $location) {
    $scope.submitSearch = function () {
      $location.url('/archive/search/?q=' + $scope.searchTerm);
    };
  });
