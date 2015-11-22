# snotes20 - frontend

## Setup

### Preconditions
- For Ubuntu 14.04:
```
$ sudo apt-get install npm ruby ruby-dev nodejs-legacy git
```

### Installation Instructions
```
$ sudo npm install -g bower grunt grunt-cli
$ sudo gem install compass
$ cd snotes20-angular-webapp
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
