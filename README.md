# Server Pack Manager

A simple Python program to run before server start to automatically merge and update the server resource pack.

## Usage
1. Clone this repo into your root server directory
2. Place all your packs into a folder called `resourcepacks`
3. Install `requirements.txt` (preferably in a venv)
4. Open the TCP port set in `run-packmngr.py`
5. Save your server start script to `run.sh` (to be called by the pack manager).
6. Run `python run-packmngr.py` to start the server

## Pack Order
By default, packs are merged in the order the files are read (depending on the OS). Custom ordering is not currently possible.