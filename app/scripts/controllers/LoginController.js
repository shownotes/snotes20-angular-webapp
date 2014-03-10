'use strict';

angular.module('snotes20App')
	.controller('LoginController', function ($scope, $rootScope, LoginService) {

		$scope.reset = function () {
			$scope.login = {
				username: '',
				password: ''
			};

			$scope.register = {
				username: '',
				email: '',
				password: '',
				password2: ''
			};

			$scope.forgotpw = {
				username: '',
				email: ''
			};

			$scope.mode = 'login';
		};

		$scope.reset();

		$scope.login = function () {
			var username = $scope.username;
			var password = $scope.password;

			LoginService.login(username, password).then(
				function (user) {
					$rootScope.user = user;
					$scope.reset();
				},
				function () {
					$rootScope.user = null;
				}
			);
		};

		$scope.register = function () {
			if ($scope.mode === 'register') {
				$scope.mode = 'register';
			} else {
				// send to server..
				$scope.mode = 'login';
			}
		};

		$scope.logout = function () {
			LoginService.logout().then(
				function () {
					$rootScope.user = null;
				},
				function () {
				}
			);
		};
	});
