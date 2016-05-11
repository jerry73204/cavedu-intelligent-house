## File description

* cavedu\_house.desktop
    Desktop file for creating menu items and desktop shortcuts

* cavedu.png
    Desktop shortcut icon for cavedu\_house.desktop

## Installation

* Copy cavedu\_house.desktop to `/home/pi/.local/share/applications/cavedu_house.desktop`.

* Create an simlink on desktop `ln -s /home/pi/.local/share/applications/cavedu_house.desktop /home/pi/Desktop/cavedu_house`, and add a simlink to autostart entry `ln -s /home/pi/.local/share/applications/cavedu_house.desktop /home/pi/.config/autostart/cavedu_house.desktop`.

* Add an button entry in `/home/pi/.config/lxpanel/LXDE-pi/panels/panel`.
```
Plugin {
  type=launchbar
  Config {
    Button {
    ...
    ...
    Button {
      id=/home/pi/.local/share/applications/cavedu_house.desktop
    }
  }
}
```

* copy the icon image `cp cavedu.png /home/pi/Pictures/cavedu.png`