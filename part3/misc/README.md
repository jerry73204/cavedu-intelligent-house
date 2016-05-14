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


# Face detection algorithm:

* Original code was downloaded from:
https://github.com/tdicola/pi-facerec-box/archive/master.zip
* Chinese explaination website:
http://www.makezine.com.tw/make2599131456/153

* Trace the code by reading the chinese explaination website:

* Start by making the code work on our pi3:

The first difference between our project and their's is we use usb camera, and they use the USB camera. We change the camera to cv2.VideoCapture(0), which means the default camera. Also, we do not change the kernel options for the rpi camera. Otherwise the rpi cannot find the camera and will not boot.

Next we have to see the hardware. So we change button press into keyboard, and the door control using RPIO into a print on the screen.

Last, we want to see the pictures caught. the original project have no screen, but we add one. OpenCV function is cv2.imshow(frame);waitKey(1); the window does not renew until waitKey. waitKey(0) waits forever. waitKey(1) waits for 1 millisecond.

Now we can use a face recgonition program on RPI. We change it to our use.

The user wants screen, so we always put the camera onto screen.
The user wants to push button and start training/start recognition, so we merge train.py face\_recognition.py into one code:
the main thread prints camera onto screen.
If a button is pushed, we go into the other code.
In the other code, we keep printing the camera onto the screen, but we do training/ recognition at the same time.

To communicate with the same flag, we use global flags.
If we see a flag is up, then we do the corresponding action.
After, we set another flag, for part3 main thread to read. 

