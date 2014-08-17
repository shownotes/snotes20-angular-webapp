var winston = require('winston');

exports.exchange = 'DOCUMENT_CHATMESSAGE';
exports.handle = function (msg, content) {
    winston.info('chat message:', content);
};
