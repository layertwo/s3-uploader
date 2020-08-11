# s3-uploader

Watch folder and upload files to a S3 bucket.

## Prerequisites

* An AWS credential file (`$HOME/.aws/credentials`)
* An AWS S3 bucket
* `docker` and `docker-compose`

## How to run

```shell
export S3_BUCKET="bucket-name"  # Name of S3 bucket
export DIRECTORY="$HOME/directory"  # All files created in this directory will be uploaded to S3
docker-compose up -d
```
