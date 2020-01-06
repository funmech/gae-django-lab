## Lab code for trying out Django applications on GAE

### Always set `entrypoint`
After many trials, it is safer to say that `entrypoint` should be set always. Without this
99.99% of time Django applications in flex environment will not be created. The [document](https://cloud.google.com/appengine/docs/standard/python3/runtime)
does not suit to Django applications. It is the same that `gunicorn` has to be included in `requirements.txt`.

### Some handy setups
1. Use `django.middleware.security.SecurityMiddleware` to force HTTPS for all GAE traffics.
1. `deploy_app.sh` generates `source_tip.txt` in an app folder for tracking
   what version of code is running.
1. It is possible to just create a Django project without applications. Simply add view and other modules
   to project's path and call them from there like this structure:
   ```shell
    app.yaml
    requirements.txt
    lab
    lab/__init__.py
    lab/settings.py
    lab/urls.py
    lab/views.py
    lab/wsgi.py
   ```