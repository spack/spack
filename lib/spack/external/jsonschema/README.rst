==========
jsonschema
==========

``jsonschema`` is an implementation of `JSON Schema <http://json-schema.org>`_
for Python (supporting 2.6+ including Python 3).

.. code-block:: python

    >>> from jsonschema import validate

    >>> # A sample schema, like what we'd get from json.load()
    >>> schema = {
    ...     "type" : "object",
    ...     "properties" : {
    ...         "price" : {"type" : "number"},
    ...         "name" : {"type" : "string"},
    ...     },
    ... }

    >>> # If no exception is raised by validate(), the instance is valid.
    >>> validate({"name" : "Eggs", "price" : 34.99}, schema)

    >>> validate(
    ...     {"name" : "Eggs", "price" : "Invalid"}, schema
    ... )                                   # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    ValidationError: 'Invalid' is not of type 'number'


Features
--------

* Full support for
  `Draft 3 <https://python-jsonschema.readthedocs.org/en/latest/validate/#jsonschema.Draft3Validator>`_
  **and** `Draft 4 <https://python-jsonschema.readthedocs.org/en/latest/validate/#jsonschema.Draft4Validator>`_
  of the schema.

* `Lazy validation <https://python-jsonschema.readthedocs.org/en/latest/validate/#jsonschema.IValidator.iter_errors>`_
  that can iteratively report *all* validation errors.

* Small and extensible

* `Programmatic querying <https://python-jsonschema.readthedocs.org/en/latest/errors/#module-jsonschema>`_
  of which properties or items failed validation.


Release Notes
-------------

* A simple CLI was added for validation
* Validation errors now keep full absolute paths and absolute schema paths in
  their ``absolute_path`` and ``absolute_schema_path`` attributes. The ``path``
  and ``schema_path`` attributes are deprecated in favor of ``relative_path``
  and ``relative_schema_path``\ .

*Note:* Support for Python 3.2 was dropped in this release, and installation
now uses setuptools.


Running the Test Suite
----------------------

``jsonschema`` uses the wonderful `Tox <http://tox.readthedocs.org>`_ for its
test suite. (It really is wonderful, if for some reason you haven't heard of
it, you really should use it for your projects).

Assuming you have ``tox`` installed (perhaps via ``pip install tox`` or your
package manager), just run ``tox`` in the directory of your source checkout to
run ``jsonschema``'s test suite on all of the versions of Python ``jsonschema``
supports. Note that you'll need to have all of those versions installed in
order to run the tests on each of them, otherwise ``tox`` will skip (and fail)
the tests on that version.

Of course you're also free to just run the tests on a single version with your
favorite test runner. The tests live in the ``jsonschema.tests`` package.


Community
---------

There's a `mailing list <https://groups.google.com/forum/#!forum/jsonschema>`_
for this implementation on Google Groups.

Please join, and feel free to send questions there.


Contributing
------------

I'm Julian Berman.

``jsonschema`` is on `GitHub <http://github.com/Julian/jsonschema>`_.

Get in touch, via GitHub or otherwise, if you've got something to contribute,
it'd be most welcome!

You can also generally find me on Freenode (nick: ``tos9``) in various
channels, including ``#python``.

If you feel overwhelmingly grateful, you can woo me with beer money on
`Gittip <https://www.gittip.com/Julian/>`_ or via Google Wallet with the email
in my GitHub profile.
