# chatify
A simple asynchronous online chat based on aiohttp, websockets and vue js

## Usage:
* Common preparation:
  * `cd /directory/with/project`
    * `sudo chmod +x ./devrun.sh`

* Back-end:
  * `cd /directory/with/project/back` #${BACK_DIR}
    * `python3 -m venv ${BACK_DIR}venv`
    * `. ${BACK_DIR}/venv/bin/activte`
    * `python -m pip install -U pip`
    * `pip install wheel`
    * `pip install -r requeremnts.txt`

* Front-end:
  * `cd /directory/with/project/front` 
    * `npm i`

* Run dev back-end and front-end dev servers:
  * `cd /directory/with/project`
    * `./devrun.sh`
