from flask import Flask, current_app
from pyaddepar.addeparrequest import AddeparRequest


class InvalidSettingsError(Exception):
    pass


class Addepar(object):
    """Main class used for initialization of Flask-Addepar."""

    def __init__(self, app=None, config=None):
        self.app = None
        if app is not None:
            self.init_app(app, config)

    def init_app(self, app, config=None):
        if not app or not isinstance(app, Flask):
            raise Exception('Invalid Flask application instance')

        self.app = app

        app.extensions = getattr(app, 'extensions', {})

        if 'addepar' not in app.extensions:
            app.extensions['addepar'] = {}

        if self in app.extensions['addepar']:
            # Raise an exception if extension already initialized as
            # potentially new configuration would not be loaded.
            raise Exception('Extension already initialized')

        if not config:
            # If not passed a config then we read the connection settings
            # from the app config.
            config = app.config

        # Obtain db connection(s)
        requests = create_requests(config)

        # Store objects in application instance so that multiple apps do not
        # end up accessing the same objects.
        s = {'app': app, 'request': requests}
        app.extensions['addepar'][self] = s

    @property
    def request(self):
        """
        Return Addepar request associated with this Addepar instance.
        """
        return current_app.extensions['addepar'][self]['request']


def create_requests(config):
    """
    Given Flask application's config dict, extract relevant config vars
    out of it and establish MongoEngine connection(s) based on them.
    """
    # Validate that the config is a dict
    if config is None or not isinstance(config, dict):
        raise InvalidSettingsError('Invalid application configuration')

    # Return a single connection
    return AddeparRequest(**config["ADDEPAR"])


addepar = Addepar()
