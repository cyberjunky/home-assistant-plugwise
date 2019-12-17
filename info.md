[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)  [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.me/cyberjunkynl/)

# Plugwise Component
This component can read values from/control Plugwise circles and plugs.

## Home-Assistant Custom Component
This is a Custom Component for Home-Assistant (https://home-assistant.io)

Note:
Although it works rather well, it is still work in progress, it uses the older python-plugwise code.
And it must be made async so it plays nice when it cannot reach a plug it queries resulting in timeouts.

{% if not installed %}

### Installation

- Copy directory `custom-components/plugwise` to your `<config dir>/custom-components` directory.
- It has as dependency the 'plugwise' module from PyPi, but it will be installed automatically.
- Configure with config below.
- Restart Home-Assistant.

{% endif %}

### Usage
To use this component in your installation, add the following to your `configuration.yaml` file:

```yaml
# Example configuration.yaml entry

switch:
  - platform: plugwise
    port: /dev/ttyUSB0
    circles:
      CirclePlus: 000D6F000023711C
      Koelkast: 000D6F00001C8F33
```

Configuration variables:

- **port** (*Optional*): Port used by your plugwise stick. (default = /dev/ttyUSB0)
- **circles** (*Required*): This section tells the component which mac addresses your plugs have and which device names you want to use.

If you want to graph power consumption values you can convert the attribute of the switch into a sensor using template platform like so:


```yaml
# Example sensor.yaml entry

- platform: template
  sensors:
    circleplus_power_usage:
      friendly_name: "CirclePlus Power Usage"
      unit_of_measurement: 'Watt'
      value_template: "{{ states.switch.circleplus.attributes.current_consumption }}"
```
NOTE: works in Hass.io

### Screenshots
![alt tag](https://github.com/cyberjunky/home-assistant-plugwise/blob/master/screenshots/plugwise-switches.png?raw=true "Screenshot Plugwise Switches")
![alt tag](https://github.com/cyberjunky/home-assistant-plugwise/blob/master/screenshots/plugwise-switch.png?raw=true  "Screenshot Plugwise Switch")
![alt tag](https://github.com/cyberjunky/home-assistant-plugwise/blob/master/screenshots/plugwise-graph.png?raw=true  "Screenshot Plugwise Graph")

### Donation
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.me/cyberjunkynl/)
