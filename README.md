# This is the server for mobile app BackgroundChanger
https://github.com/volynvlad/BackgroundChanger
## Setup
The scipt setup.sh install microframework for Python flask 
http://flask.pocoo.org/
and downloads the trained deeplab models
https://github.com/tensorflow/models/tree/master/research/deeplab

chmod +x setup.sh

./setup.sh

## Running the server
python run.py
## Be careful to set your own host, post and path
In run.py, remove.py and in the app https://github.com/volynvlad/BackgroundChanger/blob/master/BackgroundChanger/app/src/main/java/com/example/backgroundchanger/activity/ProcessActivity.java
