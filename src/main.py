import os
import tempfile
import olympe
from olympe.media import download_media
from olympe.messages.ardrone3.Piloting import TakeOff, Landing
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged
from olympe.messages.ardrone3.GPSSettingsState import GPSFixStateChanged
from olympe.messages.ardrone3.PilotingSettings import MaxTilt
from olympe.messages.move import extended_move_by
from olympe.messages.camera import (
    set_camera_mode,
    set_photo_mode,
    take_photo,
    photo_progress,
)

TIMEOUT = 120
DRONE_IP = os.environ.get("DRONE_IP", "10.202.0.1")
DRONE_MEDIA_PORT = os.environ.get("DRONE_MEDIA_PORT", "80")

# Set logging level to info
olympe.log.update_config({"loggers": {"olympe": {"level": "INFO"}}})

def main():
    drone = olympe.Drone(DRONE_IP, media_port=DRONE_MEDIA_PORT)
    drone.connect(retry=3)

    set_up_drone_camera(drone)
    fly(drone)
    download_drone_media(drone)

    drone.disconnect()

def set_up_drone_camera(drone):
    """Activate drone camera, and set it up for single photo mode"""
    # Set camera mode to photo NOTE: needs to be done before takeoff for some reason
    drone(set_camera_mode(cam_id=0, value="photo")).wait()

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

def fly(drone):
    """Command the drone to takeoff, move, take photos, and land"""

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

    # Fly around and take photos, then land
    drone(MaxTilt(30)).wait().success()
    drone(extended_move_by(10, -30, -10, 0, 200, 200, 20,_timeout=TIMEOUT)).wait().success()
    drone(take_photo(cam_id=0)).wait()
    drone(extended_move_by(30, -5, -20, 0,200, 200, 20,_timeout=TIMEOUT)).wait().success()
    drone(take_photo(cam_id=0)).wait()
    drone(extended_move_by(30, 0, -5, 0,200, 200, 20,_timeout=TIMEOUT)).wait().success()
    drone(take_photo(cam_id=0)).wait()
    drone(extended_move_by(31, 21, 20, 0, 200, 200, 20,_timeout=TIMEOUT)).wait().success()
    drone(take_photo(cam_id=0)).wait()
    drone(Landing() >> FlyingStateChanged(state="landed", _timeout=TIMEOUT)).wait()
    drone(take_photo(cam_id=0)).wait()

def download_drone_media(drone):
    """Downloads drone media files into a local temporary folder"""
    
    # Create temporary folder 
    drone.media.download_dir = tempfile.mkdtemp(prefix="olympe_photo_example")
    drone(photo_progress(result="photo_saved", _policy="wait"))

    # Download all drone media files
    media_list = drone.media.list_media()
    for media in media_list:
        drone(download_media(media, integrity_check=True)).wait()

if __name__ == "__main__":
    main()