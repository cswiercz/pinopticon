# Pinopticon

Home security and monitoring with your Raspberry Pi.

Pinopticon is a Python library for managing a home security system built from a
Raspberry Pi. Connect your home's door sensors, window sensors, and cameras.
Receive alerts via email or text.

Etymology: the project name is a play on the
"[panopticon](https://en.wikipedia.org/wiki/Panopticon), a building designed
such that every part is easily observed, derived from the Greek "*pan*-",
meaning "wide" or "all", and "*-optic*", meaning "to see".

## Project Goals

The goal of Pinopticon is to implement the following features, mostly in order
of importance. Given how early we are in the project this is, of course, subject
to change.

* Phase 1 - read input sensors and alert user via phone or email
* Phase 2 - audible alarm system
* Phase 3 - camera control
* Phase 4 - iOS and [HomeKit](http://www.apple.com/ios/home/) compatibility

## Dependencies

* [gpiozero](https://gpiozero.readthedocs.io/en/v1.3.1/) - *hardware control on the RPi*
* [tornado](http://www.tornadoweb.org/en/stable/) - *future communication via phone / web*

## Authors

* Chris Swierczewski ([cswiercz](https://github.com/cswiercz))
