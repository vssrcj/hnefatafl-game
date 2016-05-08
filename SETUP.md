### This is a quick guide on how to setup this project for yourself.

It consists of two parts.  The API backend, and the Web App frontend.

### Files included

Under src/
* ai.py : AI logic
* api.py : API endpoints
* models.py transport_models.py : Models
* utils.py game_utils.py : Utils
* main.py client.py : Handlers
* app.yaml cron.yaml : Configurations
* client/\*: Web App files

### Requirements

* Python
* Google App Engine SDK for python
* Git
* Nodejs and Gulp (if creating the Web App frontend)

### Get the files

```
git clone https://github.com/vssrcj/hnefatafl-game.git
```

### Test the project

```
dev_appserver.py src
```

### Upload the project

* Before you can upload the project to Google's servers, you need to create an app at https://console.cloud.google.com

* Set the application name in ```src/app.yaml```
* Set the allowed_client_ids of the attributes of the class **HnefataflAPI** in ```src/api.py```

If you are using the Web App, do this:
  * Set the **const url** as well as the **client_id** in ```src/client/modules/google_auth.js```
  * Setup npm using ```npm install```
  * Run gulp to combined and minify all the JS modules into one file by ```gulp build-js --type production```
  
Run the following to upload:
```
  appcfg.py update src
``` 

The project will be available at:  https://APPLICATION_NAME.appspot.com
