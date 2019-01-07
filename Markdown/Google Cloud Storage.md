# Google Cloud Storage on Google App Engine

## Installing GCS
After setting up a GAE project, go to the the google cloud platform page and navigate to Settings, click *Create* under Default Cloud storage bucket. This creates a server side storage bucket with the name generated as project-id.appspot.com. (project id being the name of the gae project)

## Setting up the python Environment for GCS

### Dowloading the client library
> pip install GoogleAppEngineCloudStorageClient -t   <your_app_directory/lib>

Remeber thate you have to be in the local environment (source /env/bin/activate) and specify the *local* library - not the computers main python library

### Using the library with the dev server 
Once the cloud storage bucket has been activated and the required lib files are installed you are good to go if you are deploy the app straight to the gae cloud, 

However if your using the local development server (localhost apps), you will have to specify a link to the online cloud storage.
This can be done using:
>  dev_appserver.py --default_gcs_bucket_name [BUCKET_NAME] app.yaml