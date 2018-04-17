# Deep Hive
Tap into the hive mind with your audience and train a deep convolutional neural network live on stage.

The application consists of these pages:

##### Dashboard
This is the live dashboard displayed on the presentation screen

##### Annotation page
Your audience will visit the annotation page to do some annotations

## Model
A very simple model is used: two dense layers on top of a VGG16 backbone           

## Stack
 * Python
 * Keras (tensorflow)
 * Flask
 * Keras
 * React.js
 * D3.js
 * webpack

## Usage
#### Docker
The easiest way to run this application is via docker.

You can start all needed containers locally by running:
    
    docker-compose up

#### Standalone
To run it directly on your local machine, create and activate conda environment first

    conda env create -f /tmp/environment.yml
    source activate deeplearning
    
Start the flask application

    cd server
    ./start.sh

Start the worker containing the model
    
    python worker.py
    
You will also need a Redis instance running.
    
#### Frontend
To recompile the javascript first install the npm packages:

    npm install
    
Then run webpack to compile:

    npm run build

To start a development server (proxies /api requests to flask):

    npm run start
