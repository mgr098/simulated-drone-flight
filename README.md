<p align="center">
  <img src="/media/drone-flying.gif" alt="Drone taking off in simulator"/>
</p>


# Simulated Drone Flight ✈️

This project contains a script which remotely controls a simulated ANAFI drone in the Parrot Sphinx simulator using the Olympe SDK.  The script will fly the drone around and take some photos. Once the flight is finished and the drone has landed, the script will download all media files from the drone into a local temporary folder.

## Prerequisites ✔

* [Parrot Sphinx](https://developer.parrot.com/docs/sphinx/)
* [Python 3.8.10](https://www.python.org/downloads/) 
* [Pip](https://pip.pypa.io/en/stable/cli/pip_download/)

## Usage 🖥

### Setup ⚙️

Clone the project and navigate to the /src folder
```
git clone https://github.com/mgr098/simulated-drone-flight.git
cd simulated-drone-flight/src
```

Install dependencies
``` 
pip3 install -r requirements.txt
```
Launch the Parrot Sphinx simulator with an ANAFI drone from your terminal. Remember to change ```login```  with your actual Parrot partner FTP account and ```pass``` to the associated password.
```
sphinx "/opt/parrot-sphinx/usr/share/sphinx/drones/anafi_ai.drone"::firmware="ftp://<login>:<pass>@ftp2.parrot.biz/versions/anafi2/pc/%23latest/images/anafi2-pc.ext2.zip"
```
In another terminal do
```
parrot-ue4-forrest
```
### Run 🚗
After you have activated the python environment you can run the script from another terminal.
```
python3 main.py
```
The script should connect to the simulated drone. Once the drone has flown around  and landed, the script should download all media files from the drone server at http://10.202.0.1/#/ into a folder in your /tmp directory. The folder will have a name starting with "olympe_photo_example" containing media files.

Remember to reset Sphinx simulation between runs by running this command from another terminal.
```
sphinx-cli action -m world fwman world_reset_all
```
