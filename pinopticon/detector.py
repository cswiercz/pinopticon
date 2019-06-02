import logging

import numpy as np
import tensorflow as tf

from PIL import Image

log = logging.getLogger()
log.setLevel(logging.INFO)


class ObjectDetector:

    def __init__(
            self, model_path='/home/pi/pinopticon/data/detect.tflite',
            label_path='/home/pi/pinopticon/data/labelmap.txt', verbose=False):
        log.info('Creating tflite interpreter from model: {0}'.format(model_path))
        self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()

        # input tensors:
        #
        #     input = quantized Nx300x300x3 RBG image (values 0-255) where N is
        #     number of input images
        #
        input_details = self.interpreter.get_input_details()
        self._input_tensor_index = input_details[0]['index']
        self._input = self.interpreter.tensor(self._input_tensor_index)
        log.info('tensor input details:\n{0}'.format(input_details))

        # output tensors:
        #
        #     classes = Nx10 top-10 class labels for N input images (int)
        #     scores  = Nx10 top-10 class scores for N input images (float)
        #
        output_details = self.interpreter.get_output_details()
        self._output_classes = self.interpreter.tensor(output_details[1]['index'])
        self._output_scores = self.interpreter.tensor(output_details[2]['index'])
        log.info('tensor output details:\n{0}'.format(output_details))

        # load label map
        with open(label_path, 'r') as f:
            self.label_map = list(map(lambda s: s.strip('\n'), f.readlines()))


    def detect(self, image, threshold=0.6, verbose=False, **kwds):
        image_ = np.array(Image.fromarray(image).resize((300, 300)), dtype=np.uint8)
        self._input()[0] = image_
        self.interpreter.invoke()

        # get results from output tensors
        classes = self._output_classes()[0]
        scores = self._output_scores()[0]

        # filter out low-probability classes
        mask = scores > threshold
        classes = classes[mask]
        scores = scores[mask]
        labels = [self.label_map[int(cls)+1] for cls in classes]

        if verbose:
            s = 'detected: '
            for score, label in zip(scores, labels):
                s += '({0:.3f}, {1}), '.format(score, label)
            log.debug(s)

        return scores, labels
