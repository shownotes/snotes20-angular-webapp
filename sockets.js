var io;

exports.init = function (conf) {
    io = require('socket.io')(conf.port, {
    });

    io.on('connection', function(socket) {
        socket.on('JOIN_DOC', function (document) {
            this.join(document);
        })
    });
};

exports.emit = function (ns, name, payload) {
    io.to(ns).emit(name, payload);
};
