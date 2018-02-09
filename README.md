# onewire-sender
Send data from 1 or more DS18B20 sensors to a http endpoint on a schedule

# Setup on a Raspberry Pi:

Install librarys (https://github.com/timofurrer/w1thermsensor/blob/master/README.md)

    sudo apt-get install python-w1thermsensor

Run OneWire-Sender when Pi boots up

    Preferences => Main menu editor => Add LXSession configuration to preferences
    LXSession => Autostart
    Add Manual autostarted application
    "lxterminal -e python /path-to-your/onewire-sensor.py"

## features incoming...
Configuration file

MQTT support (think: HomeAssistant)