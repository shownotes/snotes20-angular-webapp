var amqplib = require('amqplib');
var winston = require('winston');

var conn = null;

exports.connect = function (uri, cb) {
    amqplib.connect(uri).then(function (_conn) {
        conn = _conn;
        cb();
    }, cb);
};

exports.bindExchange = function (exchange, cb) {
    conn.createChannel().then(function (ch) {
        return ch.assertExchange(exchange, 'fanout')
        .then(function () {
            return ch.assertQueue('', {exclusive: true});
        })
        .then(function (qok) {
            return ch.bindQueue(qok.queue, exchange, '').then(function () {
                return qok.queue;
            });
        })
        .then(function (queue) {
            ch.consume(queue, function (msg) {
                cb(msg, JSON.parse(msg.content.toString()));
            }, {noAck: true});
        })
        .then(function () {
            winston.info('bound to %s exchange', exchange);
        })
        .done();
    });
};
