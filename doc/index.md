<div align="center">
  <img src="./img/pinopticon.png"><br>
</div>

[![Documentation Status](https://readthedocs.org/projects/pinopticon/badge/?version=latest)](http://pinopticon.readthedocs.io/en/latest/?badge=latest)

Home security and monitoring with your Raspberry Pi. Created by
[Chris Swierczewski](https://github.com/cswiercz).

Comprehensive documentation can be found at
[http://pinopticon.readthedocs.io](http://pinopticon.readthedocs.io).

# Usage

A basic security system configuration. *(Note: this this still a proposal.)*

```python
from pinopticon import *

sys = SecuritySystem()  # create a new security system config

# define the connected systems using the
# pins they're connected to on the RPi
door = Door(21)
alarm = Speaker(73)
email_notification = Email('alice_and_bob@example.com')

# set door system to execute the alarm
# and email notification when triggered
door.add_on_trigger(alarm)
door.add_on_trigger(email_notification)

# arm the system. intruders beware!
sys.register_device(door)
sys.arm()
```

# Install

Dependencies:
* A [Raspberry Pi](https://www.raspberrypi.org)
* [Python 3](https://www.python.org)
* [Flask](http://flask.pocoo.org)
* [gpiozero](https://gpiozero.readthedocs.io)

[Download Pinopticon](https://github.com/cswiercz/pinopticon/archive/master.zip)
or open a terminal session (on your Raspberry Pi) and obtain using Git:

```
$ git clone https://github.com/cswiercz/pinopticon.git
```

Finally, open a terminal and install on your Raspberry Pi:

```
$ cd pinopticon
$ python setup.py install
```

# License

[MIT](https://github.com/cswiercz/pinopticon/blob/master/LICENSE)
