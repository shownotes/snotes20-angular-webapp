'use strict';

angular.module('snotes30App')
  .service('actionStatusGlueService', function ($timeout) {
    this.fac = function (stat, autostart) {
      var self = {};

      self.start = function () {
        stat.status = null;
        $timeout(function () {
          stat.active = true;
        }, 100);
      };

      self.resolve = function () {
        stat.active = true;
        stat.status = true;
      };

      self.reject = function () {
        stat.active = true;
        stat.status = false;
      };

      self.reset = function () {
        $timeout(function () {
          stat.active = false;
          stat.status = null;
        }, 5000);
      };

      if(autostart === undefined) autostart = true;
      if(autostart) {
        self.start();
      }

      return self;
    };
  });
