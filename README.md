<div align="center">
  <img src="./doc/img/pinopticon.png"><br>
</div>

[![Documentation Status](https://readthedocs.org/projects/pinopticon/badge/?version=latest)](http://pinopticon.readthedocs.io/en/latest/?badge=latest)

Home security and monitoring with your Raspberry Pi. Created by
[Chris Swierczewski](https://github.com/cswiercz).

# Usage

```bash
$ cd pinopticon
$ python3 pinopticon/main.py &
$ python3 pinopticon/pusher.py S3_BUCKET_NAME
```

# Install

Dependencies:
* A [Raspberry Pi](https://www.raspberrypi.org)
* [Python 3](https://www.python.org)
* [PiCamera](https://picamera.readthedocs.io/en/latest/)
* [Numpy](https://www.numpy.org/)
* [Tensorflow Lite](https://www.tensorflow.org/lite/)

# License

[MIT](https://github.com/cswiercz/pinopticon/blob/master/LICENSE)
