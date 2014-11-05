'use strict';

angular.module('snotes30App')
    .factory('docEditChatSocket', function (socketFactory, CONFIG) {
        return socketFactory({
            'ioSocket': io(CONFIG.websocketUrl)
        });
    });
