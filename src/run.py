#!/usr/bin/env python

import logging
import os
import time
import boto3
from botocore.exceptions import ClientError
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class UploadToS3(FileSystemEventHandler):
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.client = boto3.client('s3')

    def on_created(self, event):
        time.sleep(10)  # 10 seconds on Linux, else the input file is 0kb…
        logging.info("%s: uploading…", event.src_path)
        try:
            self.client.upload_file(event.src_path, self.bucket_name, os.path.basename(event.src_path))
            logging.info("%s: upload done", event.src_path)
        except ClientError as ex:
            logging.error(ex)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    if "S3_BUCKET" not in os.environ or "DIRECTORY" not in os.environ:
        logging.error("Need two env var: S3_BUCKET and DIRECTORY")
        exit(1)

    observer = Observer()
    observer.schedule(UploadToS3(os.environ["S3_BUCKET"]), os.environ["DIRECTORY"], recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
