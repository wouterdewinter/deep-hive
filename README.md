# Deep Hive
**Tap into the hive mind with your audience and train a deep convolutional neural network live on stage.**

I use this during presentations to illustrate to the basic process of (supervised) machine learning and give the audience a feel of how much (or how little) data is needed for training.

For the [Kaggle Dogs vs. Cats dataset](https://www.kaggle.com/c/dogs-vs-cats) you get about 90% accuracy in about 250 user annotations. With 25 people in your audience this typically takes less than one minute!   

More information about the design and architecture can be found in this HackerNoon article on Medium:\
[Deep Hive: Deep learning live on stage](https://hackernoon.com/deep-hive-deep-learning-live-on-stage-7d1525a55bb1)

The application has two main parts:

#### Dashboard
This is the live dashboard displayed on the presentation screen

![Dashboard screenshot](/docs/dashboard.jpg)

#### Annotation
Your audience will visit the annotation page to do some annotations

![Annotation screenshot](/docs/annotate.jpg)

## Model
A pretty simple model is used:
- VGG16 backbone
- GlobalAveragePooling2D
- Dense (256)
- Dropout
- Dense (size is number of classes)
           
## Stack
 * Python (python 3 only)
 * Keras (tensorflow)
 * Flask
 * Redis
 * React.js
 * D3.js
 * Webpack

## Usage
#### Preparing the Dogs vs Cats dataset
1. Download the `train.zip` file from [Kaggle Dogs vs. Cats dataset](https://www.kaggle.com/c/dogs-vs-cats)
2. Unzip it in the data directory. It should create a `train` folder
3. Preprocess the images using

   ```
   python preprocess.py data/train data/catsdogs
   ```

#### Custom datasets
You can use your own dataset. The model is a classifier so the application expects the folders in the data directory to have the names of the classes. Specify the data directory with `IMAGE_PATH` in the `Config.py` file,

The application needs the images to be in a fixed size (default is 128x128). You can use the `preprocess.ipynb` notebook to rescale the images to the preferred size.

#### Custom url
To change the url displayed for the audience on the dashboard edit the `short_url` parameter in `src/config.json` file and recompile the frontend (see Frontend section).

#### Docker
The easiest way to run this application is via docker.

You can start all needed containers locally by running:
    
    docker-compose up
    
When docker is running, the dashboard can be found at:\
[http://localhost:5000/dashboard](http://localhost:5000/dashboard)

And the annotation interface at:\
[http://localhost:5000/](http://localhost:5000/)

#### Standalone
To run it directly on your local machine, create and activate conda environment first

    conda env create -f environment.yml
    source activate deephive
    
Start the flask application

    cd server
    ./start.sh

Start the worker containing the model
    
    python worker.py
    
You will also need a Redis instance running.
    
#### Frontend
To recompile the javascript first install the npm packages:

    npm install
    
For convenience, a bundle.js file has been committed in the repo. Run webpack to re-compile:

    npm run build

To start a development server (proxies /api requests to flask):

    npm run start
