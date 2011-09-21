agar
====

Agar is a set of utilities for Google App Engine, extracted from
numerous GAE projects.

Requirements
------------

Agar requires the Google App Engine SDK, webapp2, webapp2_extras,
pytz.gae, restler, and basin. Versions of these (except the Google App
Engine SDK) are located in the lib directory.

Installation
------------

To install Agar, download the source and add the agar/ directory to
your Google App Engine project. It must be on your path.

License
-------

Agar is licensed under the XYZ License. See LICENSE.txt for details.

Tests
-----

Agar comes with a set of tests. Running Agar's tests requires
unittest2 and webtest (included in the lib directory). To run them,
execute:

     run_tests.py

Testing
-------

Google App Engine now includes testbed to make local unit testing
easier. This obsoletes the GAE TestBed library. However, it had
several useful helper functions, many of which have been
re-implemented in Agar. To use them, you must use unittest2 and
inherit from agar.tests.BaseTest or agar.tests.WebTest.
