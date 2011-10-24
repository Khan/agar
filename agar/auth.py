"""
The ``agar.auth`` module contains classes, functions, and decorators to help secure a `webapp2.Requesthandler`_.
"""
from functools import wraps

from agar.config import Config


class AuthConfig(Config):
    """
    :py:class:`~agar.config.Config` settings for the ``agar.auth`` library.
    Settings are under the ``agar_auth`` namespace.

    The following settings (and defaults) are provided::

        agar_auth_AUTHENTICATION_PROPERTY = 'user'
        def agar_auth_authenticate(request):
            return None

    To override ``agar.auth`` settings, define values in the ``appengine_config.py`` file in the root of your project.
    """
    _prefix = 'agar_auth'

    #: The property name under which to place the authentication object on the request.
    AUTHENTICATION_PROPERTY = 'user'
    
    def authenticate(request):
        """
        The authenticate function. It takes a single `webapp2.Request`_ argument, and returns a value representing the
        authentication or the function can call `webapp2.abort`_ to short circuit the decorated handler. The type of
        the returned value can be anything, but it should be a type that your `webapp2.RequestHandler`_ expects.
        The default implementation always calls `webapp2.abort`_ with a status code of ``403``.

        :param request: The `webapp2.Request`_ object to authenticate.
        :return: The result of the authentication.
        """
        from webapp2 import abort
        abort(403)

#: The configuration object for ``agar.auth`` settings.
config = AuthConfig.get_config()

def authentication_required(authenticate=None, require_https=False):
    """
    A decorator to authenticate a `webapp2.RequestHandler`_.
    The decorator will assign the return value from the ``authenticate`` function to the request ``user`` attribute
    (or any re-configured name via the config :py:attr:`~agar.auth.AuthConfig.AUTHENTICATION_PROPERTY`), that is
    passed to the decorated handler. The ``authenticate`` function can call `webapp2.abort`_ if there was a problem
    authenticating the call.

    :param authenticate: The authentication function to use to authenticate a request. The function should take a single
        `webapp2.Request`_ argument, and return a value representing the authentication.
        The type of the returned value can be anything, but it should be a type that your
        `webapp2.RequestHandler`_ expects. If ``None``, the configured function
        :py:meth:`~agar.auth.AuthConfig.authenticate` will be used. If there is a problem authenticating the call, the
        function can call `webapp2.abort`_ to short circuit the decorated handler.
    :param require_https: If ``True``, this will enforce that a request was made via HTTPS, otherwise a ``403`` response
        will be returned.
    """
    if authenticate is None:
        authenticate = config.authenticate
    def decorator(request_method):
        @wraps(request_method)
        def wrapped(self, *args, **kwargs):
            if require_https:
                import urlparse
                from agar.env import on_server
                scheme, netloc, path, query, fragment = urlparse.urlsplit(self.request.url)
                if on_server and scheme and scheme.lower() != 'https':
                    self.abort(403)
            setattr(self.request, config.AUTHENTICATION_PROPERTY, authenticate(self.request))
            request_method(self, *args, **kwargs)
        return wrapped
    return decorator

def https_authentication_required(authenticate=None):
    """
    A decorator to authenticate a secure request to a `webapp2.RequestHandler`_.
    """
    return authentication_required(authenticate=authenticate, require_https=True)
