
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

TBD

## License

The s3Scanner extension is licensed under the terms of the MIT
license and is available for free.

## Links

The crawler i based on dmahugh [crawlerino](https://github.com/dmahugh/crawlerino)
The s3 scanner is based on jordanpotti [AWSBucketDump](https://github.com/jordanpotti/AWSBucketDump/)
