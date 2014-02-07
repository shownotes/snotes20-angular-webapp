angular.module('snotes20App')
  .service('LoginService', function ($q, $cookies, $rootScope) {

    /** Try to authenticate the user.
     * @param username
     * @param password
     * @return {external:Promise}
    */
    this.login = function (username, password) {
      var deferred = $q.defer();

      $cookies.login = username;

      deferred.resolve({
        name: username,
        groups: [ { longname: "team" }, { longname: "ts" } ]
      });

      return deferred.promise;
    };

    this.checkLogin = function () {
      var deferred = $q.defer();

      if($cookies.login) {
        deferred.resolve({
          name: $cookies.login,
          groups: [ { longname: "team" }, { longname: "ts" } ]
        });
      } else {
        deferred.reject(false);
      }

      return deferred.promise;
    };

    /** Try to de-authenticate the user.
     * @return {external:Promise}
     */
    this.logout = function () {
      var deferred = $q.defer();

      delete $cookies.login;

      deferred.resolve(true);
      return deferred.promise;
    };

    /** Try to register a new account.
     * @return {external:Promise}
     */
    this.register = function (username, emai, password) {
      var deferred = $q.defer();
      deferred.resolve(true);
      return deferred.promise;
    };
  });