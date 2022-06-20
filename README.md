# Flightpath Simulation

This project contains an implementation of a flighpath for a simulated ANAFI drone in the Parrot Sphinx simulator using the Olympe SDK.  The Flighthpath will fly the drone around and take some pictures.

## Prerequisites

* [Parrot Sphinx](https://developer.parrot.com/docs/sphinx/)
* [Python 3.8.10](https://www.python.org/downloads/) ?
* [Pip](https://pip.pypa.io/en/stable/cli/pip_download/)

## Installation


```sh 
pip3 install -r requirements.txt
```

## Usage

Launch the Parrot Sphinx simulator with an ANAFI drone
```
sphinx "/opt/parrot-sphinx/usr/share/sphinx/drones/anafi_ai.drone"::firmware="ftp://<login>:<pass>@ftp2.parrot.biz/versions/anafi2/pc/%23latest/images/anafi2-pc.ext2.zip"
parrot-ue4-empty
```

Run the flighpath script
```
python3 src/main.py
```

