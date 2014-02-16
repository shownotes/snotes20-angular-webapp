// http://geniuscarrier.com/ng-toggle-in-angularjs/
angular.module('snotes20App', [])
	.controller('AppCtrl',['$scope', function($scope){
		$scope.menu = true;
		$scope.toggleMenu = function() {
			$scope.menu = $scope.menu === false ? true: false;
		};
}]);