'use strict';

angular.module('snotes30App')
    .factory('docChatSocket', function (socketFactory, CONFIG) {
        return socketFactory({
            'ioSocket': io(CONFIG.websocketUrl)
        });
    });
