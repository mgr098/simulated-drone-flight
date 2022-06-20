import olympe
import os
import time
import math
import logging

from olympe.messages.ardrone3.Piloting import TakeOff, Landing
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged
from olympe.messages.ardrone3.GPSSettingsState import GPSFixStateChanged
from olympe.messages.ardrone3.PilotingSettings import MaxTilt
from olympe.messages.ardrone3.Piloting import moveBy
from olympe.messages.move import extended_move_by

DRONE_IP = os.environ.get("DRONE_IP", "10.202.0.1")
TIMEOUT = 120

olympe.log.update_config({"loggers": {"olympe": {"level": "WARNING"}}})

def test_takeoff():

    drone = olympe.Drone(DRONE_IP)
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
        
        drone (
            drone(extended_move_by(10, -30, -10, 0, 200, 200, 20,_timeout=TIMEOUT)).wait().success()
            >> drone(MaxTilt(30)).wait().success()
            >> drone(extended_move_by(30, -5, -20, 0,200, 200, 20,_timeout=TIMEOUT)).wait().success()
            >> drone(extended_move_by(30, 0, -5, 0,200, 200, 20,_timeout=TIMEOUT)).wait().success()
            >> drone(extended_move_by(31, 21, 20, 0, 200, 200, 20,_timeout=TIMEOUT)).wait().success()
            moveBy(10, 0, 0, 0)
            >> FlyingStateChanged(state="hovering", _timeout=5)
            >> Landing()

        )

        print("async stuff my G")
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
        # drone(Landing() >> FlyingStateChanged(state="landed", _timeout=5)).wait()
        # print("Landed\n")



if __name__ == "__main__":
    test_takeoff()