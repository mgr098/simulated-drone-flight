import olympe
import os
from olympe.messages.ardrone3.Piloting import TakeOff, moveBy, Landing
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged
import time

DRONE_IP = os.environ.get("DRONE_IP", "10.202.0.1")



def test_moveby2():
    drone = olympe.Drone(DRONE_IP)
    drone.connect()

    assert drone(
        TakeOff()
        >> FlyingStateChanged(state="hovering")

    ).wait().success()
    
    start = time.time()

    print("test123")
    assert drone(
        moveBy(2, 1, 3, 10, _timeout=60)
        # >> FlyingStateChanged(state="hovering", _timeout=15)

    ).wait().success()
    

    total = time.time() - start

    print("tt" + str(total))
    print("am here")

    assert drone(Landing()).wait().success()

    drone.disconnect()


if __name__ == "__main__":
    test_moveby2()