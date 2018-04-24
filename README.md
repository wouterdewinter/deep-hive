# Deep Hive
**Tap into the hive mind with your audience and train a deep convolutional neural network live on stage.**

I use this to illustrate to illustrate the basic process of (supervised) machine learning and give the audience a feel of how much (or how little) data is needed for training.

For the [Kaggle Dogs vs. Cats dataset](https://www.kaggle.com/c/dogs-vs-cats) we get about 90% accuracy in about 250 user annotation. With 25 people in your audience this takes less than one minute!   

The application has two main parts:

#### Dashboard
This is the live dashboard displayed on the presentation screen
[Dashboard screenshot](docs/dashboard.png)

#### Annotation
Your audience will visit the annotation page to do some annotations
[Annotation screenshot](docs/annotate.png)

## Model
A pretty simple model is used:
- VGG16 backbone
- GlobalAveragePooling2D
- Dense (256)
- Dropout
- Dense (size is number of classes)
           
## Stack
 * Python
 * Keras (tensorflow)
 * Flask
 * Redis
 * React.js
 * D3.js
 * Webpack

## Usage
#### Custom datasets
You can use your own dataset. The model is a classifier so the application expects the folders in the data directory to have the names of the classes. Specify the data directory with `IMAGE_PATH` in the `Config.py` file,

The application needs the images to be in a fixed size (default is 128x128). You can use the `preprocess.ipynb` notebook to rescale the images to the preferred size.

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
