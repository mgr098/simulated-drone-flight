import olympe
import os
import time
import math
import tempfile
import logging
from olympe.media import download_media, indexing_state
from olympe.messages.ardrone3.Piloting import TakeOff, Landing
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged
from olympe.messages.ardrone3.GPSSettingsState import GPSFixStateChanged
from olympe.messages.ardrone3.PilotingSettings import MaxTilt
from olympe.messages.ardrone3.Piloting import moveBy
from olympe.messages.move import extended_move_by
from olympe.messages.camera import (
    set_camera_mode,
    set_photo_mode,
    take_photo,
    photo_progress,
)

DRONE_IP = os.environ.get("DRONE_IP", "10.202.0.1")
DRONE_MEDIA_PORT = os.environ.get("DRONE_MEDIA_PORT", "80")
TIMEOUT = 120


olympe.log.update_config({"loggers": {"olympe": {"level": "INFO"}}})

def main():

    drone = olympe.Drone(DRONE_IP, media_port=DRONE_MEDIA_PORT)
    drone.connect(retry=3)
    fly(drone)
    drone.disconnect()

def fly(drone):
        # Takeoff, fly, land, ...
        print("Takeoff if necessary...")
        drone(
            FlyingStateChanged(state="hovering", _policy="check")
            | FlyingStateChanged(state="flying", _policy="check")
            | (
                GPSFixStateChanged(fixed=1, _timeout=TIMEOUT, _policy="check_wait")
                >> (
                    TakeOff(_no_expect=True)
                    & FlyingStateChanged(
                        state="hovering", _timeout=TIMEOUT, _policy="check_wait"
                    )
                )
            )
        ).wait()

        drone(set_camera_mode(cam_id=0, value="photo")).wait()
        drone.media.download_dir = tempfile.mkdtemp(prefix="olympe_photo_example")

        drone(photo_progress(result="photo_saved", _policy="wait"))

        drone(take_photo(cam_id=0)).wait()

        media_list = drone.media.list_resources(None)
        media_list = drone.media.list_media()
        print("@" + str(media_list))
        # print(drone.media.media_info(media_list[0]))
        print(drone.media.media_info("AAAA_1"))
        # print(drone.media.resource_info(media_list[0]))
        print(drone.media.resource_info("AAAA_1"))

        drone(download_media("AAAA_1", integrity_check=True)).wait()

        # try:
        # except:
        #     drone(download_media("AAAA_0000001_1.MP4", integrity_check=True))
        #     drone(download_media(media_list[0], integrity_check=True))




        # drone(moveBy(2, 0, 0, 0, _timeout=TIMEOUT)).wait().success()
        # drone(Landing() >> FlyingStateChanged(state="landed", _timeout=5)).wait()





        # >> Landing()
        # print("Moving 1/4")
        # drone(MaxTilt(30)).wait().success()
        # drone(extended_move_by(10, -30, -10, 0, 200, 200, 20,_timeout=120)).wait().success()
        # print("Moving 2/4")
        # drone(extended_move_by(30, -5, -20, 0,200, 200, 20,_timeout=120)).wait().success()
        # print("Moving 3/4")
        # drone(extended_move_by(30, 0, -5, 0,200, 200, 20,_timeout=120)).wait().success()
        # print("Moving 3/4")
        # drone(extended_move_by(31, 21, 20, 0, 200, 200, 20,_timeout=120)).wait().success()
        # print("Landing...")
        # print("Landed\n")



if __name__ == "__main__":
    main()