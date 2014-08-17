# snotes20-realtime
Handles all realtime connections in the snotes20-webapp. The communication with the main app is done via AMQP.

## Setup
Copy `config.json.example` to `config.json`, adapt values as necessary, run using your favorite node deamon tool or
simply by executing `node main.js`.

## Structure
* `main.js`, contains initialization code and loading of handlers
* `rbbit.js`, contains all directly amqp-related code
* `handlers`, a directory containing the handlers as individual files

## Handlers
For each exchange in rabbitmq one or more handlers can be defined. They are files in `./handlers/` (or any other dir, if
set in config). All handlers in the directory are loaded automatically.

A basic handler implementation:
```javascript
exports.exchange = 'EXCHANGE_NAME';
exports.handle = function (msg, content) {
  // msg      is the full message from amqplib
  // content  is the decoded and parsed JSON-body of the message as javascript-object
};
```
