import logging
import os
import os.path
import time

import boto3

from botocore.exceptions import ClientError

log = logging.getLogger()
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())


ONE_MINUTE = 60
ONE_HOUR = 60 * ONE_MINUTE
ONE_DAY = 24 * ONE_HOUR
ONE_WEEK = 7 * ONE_DAY

class BucketUploader:

    def __init__(self, bucket, profile_name='default', region_name='us-west-2'):
        self.session = boto3.Session(
            profile_name=profile_name, region_name=region_name)
        self.s3 = self.session.client('s3')
        self.bucket = bucket


    def upload_file(self, filename):
        object_name = os.path.split(filename)[-1]

        log.info('uploading {0} to {1}/{2}'.format(
            filename, self.bucket, object_name))
        try:
            self.s3.upload_file(filename, self.bucket, object_name)
        except ClientError as e:
            log.error(e)
            return False
        return True


class Pusher:

    def __init__(self, directory_name, bucket_uploader):
        directory_name = os.path.abspath(directory_name)
        if not os.path.isdir(directory_name):
            raise ValueError('{0} is not a directory'.format(director_name))

        self.directory_name = directory_name
        self.bucket_uploader = bucket_uploader

    def listen(self, max_duration=float('inf'), sleep_time=ONE_HOUR):
        log.info('listening to changes in {0} at {1} second intervals for {2} '
                 'seconds'.format(self.directory_name, sleep_time, max_duration))

        listening_start_time = time.time()
        duration = 0.0
        while duration < max_duration:
            log.info('sleeping for {0} seconds...'.format(sleep_time))
            time.sleep(sleep_time)

            filenames = os.listdir(self.directory_name)
            log.info('found files: {0}'.format(filenames))
            for filename in filenames:
                filename = os.path.join(self.directory_name, filename)
                response = self.bucket_uploader.upload_file(filename)
                if response is False:
                    log.error('unable to upload {0}. Will not delete!'.format(
                        filename))
                else:
                    log.info('deleting {0}'.format(filename))
                    os.remove(filename)

            duration = time.time() - listening_start_time

        log.info('stopped listening to {0}'.format(self.directory_name))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Upload pinopticon videos to a specified S3 bucket.')
    parser.add_argument('bucket', help='The name of the target s3 bucket.')
    parser.add_argument('--profile', default='default',
                        help='Use a specific profile from your credential file. (Default: default)')
    parser.add_argument('--sleep', metavar='SECONDS', type=int, default=15*ONE_MINUTE,
                        help='Length of period to wait before checking for videos. (Default: 900)')
    args = parser.parse_args()

    bucket_uploader = BucketUploader(args.bucket, profile_name=args.profile)
    pusher = Pusher('/home/pi/pinopticon/output/', bucket_uploader)
    pusher.listen(sleep_time=args.sleep)

