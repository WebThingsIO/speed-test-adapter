# speed-test-adapter

Speed test adapter for the [Mozilla WebThings Gateway](https://iot.mozilla.org).

## Usage

Normally you will just want to install this from the add-ons list provided by the gateway.

## Data Providers

* [https://fast.com](https://fast.com)
* [https://speedtest.net](https://speedtest.net)

# Requirements

If you're running this add-on outside of the official gateway image for the Raspberry Pi, i.e. you're running on a development machine, you'll need to do the following (adapt as necessary for non-Ubuntu/Debian):

```
sudo apt install python3-dev libnanomsg-dev
sudo pip3 install nnpy
sudo pip3 install git+https://github.com/mozilla-iot/gateway-addon-python.git
```
