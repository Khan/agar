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
        The authenticate function. It takes a single `webapp2.Request`_ argument, and returns a non-``None`` value if
        the request can be authenticated. If the request can not be authenticated, the function should return ``None``.
        The type of the returned value can be anything, but it should be a type that your `webapp2.RequestHandler`_ expects.
        The default implementation always returns ``None``.

        :param request: The `webapp2.Request`_ object to authenticate.
        :return: A non-``None`` value if the request can be authenticated. If the request can not be authenticated, the
            function should return ``None``.
        """
        return None

#: The configuration object for ``agar.auth`` settings.
config = AuthConfig.get_config()

def https_authenticate(request):
    """
    An authenticate function for use with the :py:func:`~agar.auth.https_authentication_required` decorator. Enforces that a request
    was made via HTTPS.  If it was a secure request, it will defer to the config function :py:meth:`~agar.auth.AuthConfig.authenticate`.
    If not, it will return ``None``.

    :param request: The `webapp2.Request`_ object to authenticate.
    :return: A non-``None`` value if the request was made via HTTPS and can be authenticated. If the request was not made
        via HTTPS or can not be authenticated, ``None``.
    """
    import urlparse
    from agar.env import on_server
    scheme, netloc, path, query, fragment = urlparse.urlsplit(request.url)
    if on_server and scheme and scheme.lower() != 'https':
        return None
    return config.authenticate(request)

def authentication_required(authenticate=None):
    """
    A decorator to authenticate a `RequestHandler <http://webapp-improved.appspot.com/api.html#webapp2.RequestHandler>`_.
    If the authenticate function returns a non-``None`` value, it will assign it to the request ``user`` attribute
    (or any re-configured name), that is passed to the decorated handler. If the authenticate function returns ``None``,
    it will call the `webapp2.RequestHandler.abort`_ method with a status of ``403``.

    :param authenticate: The authenticate function to use to authenticate a request. The function should take a single
        `webapp2.Request`_ argument, and return a non-``None`` value if the request can be authenticated. If the request
        can not be authenticated, the function should return ``None``. The type of the returned value can be anything,
        but it should be a type that your `webapp2.RequestHandler`_ expects.
        If ``None``, the config function :py:meth:`~agar.auth.AuthConfig.authenticate` will be used.
    """
    if authenticate is None:
        authenticate = config.authenticate
    def decorator(request_method):
        @wraps(request_method)
        def wrapped(self, *args, **kwargs):
            authentication = authenticate(self.request)
            if authentication is not None:
                setattr(self.request, config.AUTHENTICATION_PROPERTY, authentication)
                request_method(self, *args, **kwargs)
            else:
                self.abort(403)
        return wrapped
    return decorator

def https_authentication_required():
    """
    A decorator to authenticate a secure request to a `webapp2.RequestHandler`_.
    This decorator uses the :py:func:`~agar.auth.https_authenticate` authenticate function.
    """
    return authentication_required(authenticate=https_authenticate)
