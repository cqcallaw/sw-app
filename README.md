# Software Homework Package

1. System Knowledge
  a. Check for networking - see connectivity-check folder
  b. Remote restart - see remote-restart folder

## Testing the Demo App

```
$ git clone https://github.com/cqcallaw/sw-app sw-app && cd sw-app
$ virtualenv venv
$ source venv/bin/activate
$ pip install -e .
$ export FLASK_ENV='development'; export FLASK_APP='auth_demo'; flask run
```