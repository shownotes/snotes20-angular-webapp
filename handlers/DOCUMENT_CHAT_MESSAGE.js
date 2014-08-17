var winston = require('winston');
var sockets = require('../sockets.js');

exports.exchange = 'DOCUMENT_CHATMESSAGE';
exports.handle = function (msg, content) {
    winston.info('chat message:', content);
    sockets.emit(content.document, 'DOCUMENT_CHATMESSAGE', content);
};
