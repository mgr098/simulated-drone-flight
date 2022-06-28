# simulated-drone-flight 

This project contains a script which remotely controls a simulated ANAFI drone in the Parrot Sphinx simulator using the Olympe SDK.  The script will fly the drone around and take some pictures. Once the flight is finished and the drone has landed, the script will download all media files from the drone into a temporary folder locally.

## Prerequisites

* [Parrot Sphinx](https://developer.parrot.com/docs/sphinx/)
* [Python 3.8.10](https://www.python.org/downloads/) 
* [Pip](https://pip.pypa.io/en/stable/cli/pip_download/)

## Installation


```sh 
pip3 install -r requirements.txt
```

## Usage

Launch the Parrot Sphinx simulator with an ANAFI drone from your terminal.
```
sphinx "/opt/parrot-sphinx/usr/share/sphinx/drones/anafi_ai.drone"::firmware="ftp://<login>:<pass>@ftp2.parrot.biz/versions/anafi2/pc/%23latest/images/anafi2-pc.ext2.zip"
parrot-ue4-forrest
```

After you have activated the environment you can run the script from another terminal.
```
python3 src/main.py
```
The script should connect to the simulated drone. Once the drone has flown around  and landed, the script should download all media files from the drone server at http://10.202.0.1/#/ into a local folder in your /tmp directory. The folder will have a name starting with "olympe_photo_example" containing image files.