
s3Scanner
======================

The repository contains a crawler, s3 scanner and the website.
I started his is a project because I looked for a reason to work with [redis](https://redis.io/) and [Flask](http://flask.pocoo.org/)

The scanner is based on three parts,
* Crawler that scan the web and report to the redis db on any suspicious bucket
* S3Scanner that looks for interesting files in the buckets
* Flask website to expose the files list to the world :-)

## Table of content

- [Installation](#installation)
- [setup](#setup)
- [Execution](#execution)
- [License](#license)
- [Links](#links)

## Installation
I'm using Ubuntu 17.04, so the installation is for Ubuntu 17.04

1. Download, Install and Run [redis server](https://redis.io/download)
```
tar -zxvf redis-4.0.2.tar.gz
cd redis-4.0.2/
make
sudo make install
redis-server &
```

2. Download and Install Flask
```
sudo pip3 install flask
```

## Setup

Edit the setup.py file with starting point
```
python3 setup.py
```

## Execution
Each process is in different shell...

1. Run the crawler in endless loop
  The request module crash from time to time due to ssl3 issues etc...
  I decided to just write a script to restart the python it's easier for this example
  ```
  ./endlessrun.sh
  ```

2. Run the s3Scanner -
  Because the scanner is much faster than the crawler I use cron to run it every hour or so ...
```
./cron.job
```

3. Run the Flask server -
```
FLASK_APP=server.py flask run
```

## License

The s3Scanner extension is licensed under the terms of the MIT
license and is available for free.

## Links

The crawler i based on dmahugh [crawlerino](https://github.com/dmahugh/crawlerino)
The s3 scanner is based on jordanpotti [AWSBucketDump](https://github.com/jordanpotti/AWSBucketDump/)
