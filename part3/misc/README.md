# Intros

## Files

* `main.py`
    The main Python script, including state-machine based impl.

* `config.py`
    The file storing configurations, such as serial port, GPIO ports.

* `constants.py`
    The file storing constants and global variables used accross multiple scripts.

* `face_auth.py`
    A threaded, async impl. of face training and recognition script.

* `gui.py`
    A threaded, async GUI interface impl. using Python TkInter.

* `mediatek_cloud.py`
    A utility script for data uploading to / downloading from MediaTek could service.

* `rfid.py`
    A utility script for handling tag data from RFID sensor.

* `haarcascade_frontalface_alt.xml`
    A config file used by face recognition algorithm.

## Code architecture

* The following considerations are taken into acconut:
    1. Sensor data should be processed in real time. Only small laetency is allowed.
    2. Face recognition algorithms contributes to most of computational-bounded tasks, while the CPU power on Pi is limited.
    3. The GUI should be "responsive". That is, latency in GUI interactions would lead to bad user experience.
    4. Some incidences of sensor events are not predictive (RFID detection, etc). Busy waiting solution is not recommended.
    5. Several developers participated in the shared code repository.

* Based on the considerations, the following solutions are applied.
    1. State-based, event-driven impl. The algorithm goes like
    ```
    loop
    {
        if check_event_1:
            call handle_event_1()
            state = new_state
        elif check_event_2:
            call handle_event_2()
            state = new_state
        ...
    }
    ```

    2. To avoid code being blocked by sensor reading or writing, and face detection tasks, the program is written in threaded manner. You might interested in `worker()` functions in `rfid.py`, `face_auth.py` and `gui.py`. Note that if performance counts, N x Python threads won't achieve N times performance because of GIL. There are alternatives to threads for simpler tasks, such as `select()` or non-blocking file reading.

    3. GIT is used to achieve better cooperation between several developers.

## Files for deployment

* `thhs_house.desktop`
    Desktop file for creating menu items and desktop shortcuts

* `thhs.png`
    Desktop shortcut icon for thhs\_house.desktop

* `autossh.service`
    Systemd service file for establishing ssh tunnel to wtf.csie.org using autossh. This file is intended for maintenance purpose.

* `ping.service`
    Systemd service file for send pings to wtf.csie.org. This file is intended for maintenance purpose.

## Installation

* Asumed the Raspbian Wheezy distro. The following instructions are tested on Raspberry Pi 2 & 3.

* Make sure the autossh package is installed. Run `sudo aptitude install autossh` to install this package.

* Copy thhs\_house.desktop to `/home/pi/.local/share/applications/thhs_house.desktop`.

* Create an simlink on desktop `ln -s /home/pi/.local/share/applications/thhs_house.desktop /home/pi/Desktop/thhs_house`, and add a simlink to autostart entry `ln -s /home/pi/.local/share/applications/thhs_house.desktop /home/pi/.config/autostart/thhs_house.desktop`.

* Add an button entry in `/home/pi/.config/lxpanel/LXDE-pi/panels/panel`.
```
Plugin {
  type=launchbar
  Config {
    Button {
    ...
    ...
    Button {
      id=/home/pi/.local/share/applications/thhs_house.desktop
    }
  }
}
```

* Copy the icon image `cp thhs.png /home/pi/Pictures/thhs.png`

* Copy both autossh.service and ping.service to `/lib/systemd/system/{autossh.service,ping.service}`, and then run `systemctl daemon-reload` to load service files.

* Run `systemctl start autossh.service` to start autossh, and also for ping service `systemctl start ping.service`. To make these services started on boot, run `systemctl enable autossh.service` and similarly for ping.service.

# Technical details

## Face detection algorithm

Check `face_auth.py` for complete source code.

* Original source code was downloaded from [https://github.com/tdicola/pi-facerec-box/archive/master.zip](https://github.com/tdicola/pi-facerec-box/archive/master.zip).

* Chinese explaination website [http://www.makezine.com.tw/make2599131456/153](http://www.makezine.com.tw/make2599131456/153). Trace the code by reading the Chinese article.

* The orignial source code should be modified to support USB camera capturing, which is done by `cv2.VideoCapture(0)` using cv2 module.

* For those cv2 commands used in our code, please refer to OpenCV docs for more details.

* A way to test the performance of processed is to show images by `cv2.imshow(frame)` and then `cv2.waitkey(1)`. `cv2.waitkey(1)` makes the program sleep for 1ms, while `cv2.waitkey(0)` waits forever until a key is pressed.

## MediaTek could service (MCS) communication

Check `mediatek_cloud.py` for complete source code.

* A public API interface is provided by MCS. Since no Python examples provided on MCS website, we refer to the raw HTTP request data and create a Python script from scratch.

## RFID sensor

Check `rfid.py` for complete source code.

* The RFID sensor provides a serial port interface for communication with configurations 9600 baudrate, 8 data bits, 1 stop bit, and no verify bit. Refer to [http://www.seeedstudio.com/wiki/Grove\_-\_125KHz\_RFID\_Reader](http://www.seeedstudio.com/wiki/Grove_-_125KHz_RFID_Reader) for techical details.

* By setting the sensor to UART mode, a 14-byte data formatted in `[start byte][12 byte tag data][end byte]` will be sent when a tag is detected.
