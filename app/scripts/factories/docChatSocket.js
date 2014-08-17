'use strict';

angular.module('snotes30App')
    .factory('docChatSocket', function (socketFactory) {
        return socketFactory({
            'ioSocket': io('http://localhost:5133')
        });
    });
