# avroscore
Avro is a great data serialization framework but there are limited tools for processing Avro data via the command line. Avroscore brings the robust, powerful functionality of underscore.js to Avro.

Requirements
------------
To use Avroscore, you'll need to have [fastavro](https://pypi.python.org/pypi/fastavro/) and [underscore-cli](https://github.com/ddopson/underscore-cli) installed.

```bash
pip install fastavro
```

```bash
npm install -g underscore-cli
```

Installation
------------

TBD

Usage
-----

Avroscore supports all the functionality of both fastavro/avrocat and underscore-cli.

Try it out with some example data:

```bash
avroscore -d example/episodes.avro pluck air_date
```
