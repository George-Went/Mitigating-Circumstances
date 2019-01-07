# Flask

## Installing Flask

### Setting up Virtual Environments 

A virtual python environment (venv) can be used to install different version of packages that your computrer alreasdy has installed, virtual python environments can be installed using:

```
pip install virtualenv
```
To create the virtual environent to run the project on, use 
```
virtualenv <name of virtual environment>
```

You can enter the virtual environment by using 
```
source ~/<name of venv>/bin/activate
```
This will set your source as the virtual python environment - independent from the python that is running on your machine 

### Installing Flask 
```
pip install flask
```

## Setting up flask to run on Google App Engine 

The first part of a GAE application is the app.yaml files, these are used to denote the packages and handlers used in the applicaiton.

```yaml
runtime: python27
api_version: 1
threadsafe: true


handlers:
- url: /static
  static_dir: static
- url: /.*
  script: main.app

```

Due to the way flask works, templates and css files will automatically be expected to be found in their respective "template" and "static" directories

Another file expected is the appengine_config.py file - this denotes the third party packages can be found, so that GAE can run them - it is standard to create a 'lib' directory in the project - if this is not done then errors such as "no such virtual env" can be gotten - meanign that google cant find the third party apps 

Example appengine_config.py file
```python
from google.appengine.ext import vendor

# Add any libraries installed in the "lib" folder.
vendor.add('lib') #Denotes the directory to find the libraries in 
```

The Last part of a basic application needed to run is the main.py file,this is used as a root for the applictation, in a similar fashion to java based programs. 

Below is an example Hello World program in flask 

```python 
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
```

## Running a application 

### Running on a local host
You can run an application on a local host to test out new features - when saving code, the local environment will update automatically 

when running on a local hosdt, any third party addons not allready installed as part of the dev_appserver suit will have to be in a /lib file and installed into the local virtual environment

To run on local host (8080) use:
```
dev_appserver.py app.yaml
```

### Running on google app engine 

## Installing 3rd party libraries 

Due to the way google app engine works, a collection of common 3rd party libraries are installed within the system and the local test environment, however any extra 3rd party libraries such as flask addons like flask-login and wtf-forms will have to be installed under /lib


*note* just istalling the files using pip is not enough as it will install then on your main system, not in the /lib directory

*note2* make sure that your running on the virtual environment when dowloading / running the application, as this will move your source files to a location within the environemnt, which can then be used by the google dev_appserver 

```
pip install -t lib/ <library-name>
```