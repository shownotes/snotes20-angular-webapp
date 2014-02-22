// http://geniuscarrier.com/ng-toggle-in-angularjs/
angular.module('snotes20App', [])
	.controller('AppCtrl',['$scope', function($scope){
		'use strict';
		$scope.menu = true;
		$scope.toggleMenu = function() {
			$scope.menu = $scope.menu === false ? true: false;
		};
	}]);
