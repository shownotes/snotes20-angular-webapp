var fs = require('fs');
var winston = require('winston');
var nconf = require('nconf');

nconf.argv()
     .env()
     .file({ file: './config.json' });


var rbbit = require('./rbbit.js');

rbbit.connect(nconf.get('amqp:uri'), function () {
    winston.info('amqp connected!');

    var handlerDir = nconf.get('handlers:dir');

    fs.readdir(handlerDir, function (err, files) {
        for(var i = 0; i < files.length; i++) {
            var handler = require(handlerDir + files[i]);
            rbbit.bindExchange(handler.exchange, handler.handle);
        }
    })
});

var sockets = require('./sockets.js');

sockets.init(nconf.get('sockets'));
