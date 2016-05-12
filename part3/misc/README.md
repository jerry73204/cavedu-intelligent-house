## File description

* cavedu\_house.desktop
    Desktop file for creating menu items and desktop shortcuts

* cavedu.png
    Desktop shortcut icon for cavedu\_house.desktop

* autossh.service
    Systemd service file for starting autossh. This file is intended for maintenance purpose.

* ping.service
    Systemd service file for starting ping. This file is intended for maintenance purpose.

## Installation

* Asume the Raspbian distro. The following instructions is tested on Raspbian wheezy on Raspberry Pi 2 & 3.

* Make sure the autossh package is installed. Run `sudo aptitude install autossh` to install this package.

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

* Copy the icon image `cp cavedu.png /home/pi/Pictures/cavedu.png`

* Copy both autossh.service and ping.service to `/lib/systemd/system/{autossh.service,ping.service}`, and then run `systemctl daemon-reload` to load service files.

* Run `systemctl start autossh.service` to start autossh, and also for ping service `systemctl start ping.service`. To make these services started on boot, run `systemctl enable autossh.service` and similarly for ping.service.
