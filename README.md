# Software Auth Demo Package

1. System Knowledge
  a. Check for networking - see connectivity-check folder
  b. Remote restart - see remote-restart folder

## Testing the Demo App

```
$ git clone https://github.com/cqcallaw/sw-app sw-app && cd sw-app # clone project
$ virtualenv venv # setup virtual environment
$ source venv/bin/activate # activiate virtual environment
$ pip install -e . # install dependencies
$ nosetests # run tests
$ pylint auth_demo tests # run linting
$ export FLASK_ENV='development'; export FLASK_APP='auth_demo'; flask run # run app
```

App should be available at http://localhost:5000/