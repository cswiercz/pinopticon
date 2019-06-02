#!/usr/bin/env python3

import io
import logging
import shutil
import time

import numpy as np
import picamera
import picamera.array

from detector import ObjectDetector

log = logging.getLogger()
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())


resolution = (640, 480) #(1280, 720)
framerate = 12
output_frame = np.empty((resolution[1], resolution[0], 3), dtype=np.uint8)


def detect_labels(camera, model, target_label='person'):
    global output_frame
    camera.capture(output_frame, 'rgb', use_video_port=True)
    scores, labels = model.detect(output_frame)
    # with picamera.array.PiRGBArray(camera, size=(300, 300)) as output:
    #     camera.capture(output, 'rgb', resize=(300, 300), use_video_port=True)
    #     scores, labels = model.detect(output.array)

    if target_label in labels:
        return True
    return False


def stream_loop(camera, stream, model, target_label='person'):
    args = (camera, model)
    kwds = dict(target_label=target_label)
    while True:
        camera.wait_recording(1)

        if detect_labels(*args, **kwds):
            filename = time.asctime().replace(' ', '-').replace(':', '-')
            filename += '.h264'

            log.info('{0} detected. recording to {1}...'.format(target_label, filename))
            camera.split_recording(filename)
            stream.clear()

            # check for a person every five seconds. if after six tries there
            # is no person then stop recording. we also stop recording after a
            # maximum duration (10 minutes)
            detected_person = True
            max_loops = 2 * 10
            while detected_person:
                camera.wait_recording(5)
                detected_person = detect_labels(*args, **kwds)

                max_loops -= 1
                if max_loops <= 0:
                    log.info('exceeded maximum recording time!')
                    detected_person = False

            log.info('resuming stream...'.format(target_label))
            shutil.move(filename, '/home/pi/pinopticon/output/' + filename)
            camera.split_recording(stream)


def main():
    log.info('============================================================\n'
             '======================== Pinopticon ========================\n'
             '============================================================')

    log.info('initializing object detection model...')
    model = ObjectDetector()

    log.info('setting up camera and stream...')
    with picamera.PiCamera() as camera:
        camera.resolution = resolution
        camera.framerate = framerate
        stream = picamera.PiCameraCircularIO(camera, seconds=10)
        camera.start_recording(stream, format='h264')
        try:
            log.info('starting main loop...')
            stream_loop(camera, stream, model)
        finally:
            camera.stop_recording()


if __name__ == '__main__':
    main()
