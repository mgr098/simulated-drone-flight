from statistics import mode
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

#TODO:
# Restructure code
# Fly while taking photo ascync
# Fly without stopping
# Fly without stopping while taking photos
# Fly while streaming, look into livestream
# Fly and use different camera modes (at the same time? while streaming?)

TIMEOUT = 120
DRONE_IP = os.environ.get("DRONE_IP", "10.202.0.1")
DRONE_MEDIA_PORT = os.environ.get("DRONE_MEDIA_PORT", "80")

olympe.log.update_config({"loggers": {"olympe": {"level": "INFO"}}})

def main():
    drone = olympe.Drone(DRONE_IP, media_port=DRONE_MEDIA_PORT)
    drone.connect(retry=3)
    fly(drone)
    drone.disconnect()

def fly(drone):
        # Set camera mode to photo NOTE: needs to be done before takeoff for some reason
        drone(set_camera_mode(cam_id=0, value="photo")).wait()
        
        # Automatic takeoff
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

        # Set photo mode to single
        drone(
            set_photo_mode(
                cam_id=0,
                mode="single",  # any other mode might not be supported on a simulated drone
                format="rectilinear",
                file_format="jpeg",
                burst="burst_14_over_1s",  # this gets ignored in "single" photo mode
                bracketing="preset_1ev",
                capture_interval=0.0,  # this gets ignored in "single" photo mode
            )
        ).wait()

        # Crete temp folder for media download
        drone.media.download_dir = tempfile.mkdtemp(prefix="olympe_photo_example")
        drone(photo_progress(result="photo_saved", _policy="wait"))

        # Fly around and take photos
        drone(MaxTilt(30)).wait().success()
        drone(extended_move_by(10, -30, -10, 0, 200, 200, 20,_timeout=120)).wait().success()
        drone(take_photo(cam_id=0)).wait()
        drone(extended_move_by(30, -5, -20, 0,200, 200, 20,_timeout=120)).wait().success()
        drone(take_photo(cam_id=0)).wait()
        drone(extended_move_by(30, 0, -5, 0,200, 200, 20,_timeout=120)).wait().success()
        drone(take_photo(cam_id=0)).wait()
        drone(extended_move_by(31, 21, 20, 0, 200, 200, 20,_timeout=120)).wait().success()
        drone(take_photo(cam_id=0)).wait()
        drone(Landing(_timeout=TIMEOUT)).wait().success()
        drone(take_photo(cam_id=0)).wait()

        # Download all drone media files
        media_list = drone.media.list_media()
        for media in media_list:
            drone(download_media(media, integrity_check=True)).wait()

if __name__ == "__main__":
    main()