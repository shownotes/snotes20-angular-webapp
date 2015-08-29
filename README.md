# snotes20 - frontend

## Setup

```
$ npm install -g bower grunt grunt-cli
$ gem install compass
$ cd snotes20
$ npm install
$ bower install
  # copy app/components/config_dev.js.sample to config_dev.js and config_dist.js
  # and adapt apiBaseUrl & mediaUrl
```

## Development Server

```
$ grunt serve
```

Note: this will use `config_dev.js`.

## Building


```
$ grunt build
```

The resulting files are saved in the `dist/`-directory.

Note: this will use `config_dist.js`, which file will **not** be minifed.
