'use strict';

angular.module('snotes30App')
    .factory('docEditChatSocket', function (socketFactory, CONFIG) {
        return socketFactory({
            'ioSocket': io.connect(CONFIG.websocket.host, {path: CONFIG.websocket.path})
        });
    });
