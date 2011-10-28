Changes
-------

* **0.3dev** (Development Version) -- Not released

  * `agar.auth`_

    * **Breaking Changes**

      * The `AuthConfig`_ configuration ``authenticate`` has been renamed to `DEFAULT_AUTHENTICATE_FUNCTION`_.

      * The `authenticate function`_ is now passed the current `RequestHandler`_ rather than the
        `Request`_. The `Request`_ can still be accessed from the `RequestHandler`_ via ``handler.request``.

      * The `authentication_required`_ decorator no longer aborts with status ``403`` when the
        `authenticate function`_ returns ``None``. Instead, the decorator will simply set the `Request`_ ``user``
        attribute (or any configured `AUTHENTICATION_PROPERTY`_) to ``None``. This is useful for handlers where
        authentication is optional. Users can update their `authenticate function`_ to call `handler.abort()`_
        if they wish to keep the previous behavior.

    * Updated `DEFAULT_AUTHENTICATE_FUNCTION`_ to retain ``403`` behavior out of the box.

  * `agar.test`_

    * Added `BaseTest.get_tasks()`_.

    * Added `BaseTest.assertTasksInQueue()`_.

    * Added `BaseTest.clear_datastore()`_.

    * Added `WebTest.assertUnauthorized()`_.

    * Added `WebTest.put()`_.

    * Added `WebTest.delete()`_.

* **0.2** (First Public Release) -- 2011-10-14

  * Updated docs

* **0.1** (Development Version Only) -- 2011-09-21


.. Links

.. _Request: http://webapp-improved.appspot.com/api/webapp2.html#webapp2.Request
.. _RequestHandler: http://webapp-improved.appspot.com/api/webapp2.html#webapp2.RequestHandler
.. _handler.abort(): http://webapp-improved.appspot.com/api/webapp2.html#webapp2.RequestHandler.abort

.. _agar: http://packages.python.org/agar/agar.html
.. _agar.auth: http://packages.python.org/agar/agar.html#module-agar.auth
.. _agar.test: http://packages.python.org/agar/agar.html#module-agar.test
.. _AuthConfig: http://packages.python.org/agar/agar.html#agar.auth.AuthConfig
.. _authentication_required: http://packages.python.org/agar/agar.html#agar.auth.authentication_required
.. _authenticate function: http://packages.python.org/agar/agar.html#agar.auth.AuthConfig.authenticate
.. _AUTHENTICATION_PROPERTY: http://packages.python.org/agar/agar.html#agar.auth.AuthConfig.AUTHENTICATION_PROPERTY
.. _DEFAULT_AUTHENTICATE_FUNCTION: http://packages.python.org/agar/agar.html#agar.auth.AuthConfig.DEFAULT_AUTHENTICATE_FUNCTION
.. _BaseTest.clear_datastore(): http://packages.python.org/agar/agar.html#agar.test.BaseTest.clear_datastore
.. _BaseTest.get_tasks(): http://packages.python.org/agar/agar.html#agar.test.BaseTest.get_tasks
.. _BaseTest.assertTasksInQueue(): http://packages.python.org/agar/agar.html#agar.test.BaseTest.assertTasksInQueue
.. _WebTest.assertUnauthorized(): http://packages.python.org/agar/agar.html#agar.test.WebTest.assertUnauthorized
.. _WebTest.put(): http://packages.python.org/agar/agar.html#agar.test.WebTest.put
.. _WebTest.delete(): http://packages.python.org/agar/agar.html#agar.test.WebTest.delete
