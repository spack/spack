
ruamel.yaml
===========

``ruamel.yaml`` is a YAML 1.2 loader/dumper package for Python.

* `Overview <http://yaml.readthedocs.org/en/latest/overview.html>`_
* `Installing <http://yaml.readthedocs.org/en/latest/install.html>`_
* `Details <http://yaml.readthedocs.org/en/latest/detail.html>`_
* `Examples <http://yaml.readthedocs.org/en/latest/example.html>`_
* `Differences with PyYAML <http://yaml.readthedocs.org/en/latest/pyyaml.html>`_

.. image:: https://readthedocs.org/projects/yaml/badge/?version=stable
   :target: https://yaml.readthedocs.org/en/stable

ChangeLog
=========

::

  0.11.15 (2016-XX-XX):
    - Change to prevent FutureWarning in NumPy, as reported by tgehring
    ("comparison to None will result in an elementwise object comparison in the future")

  0.11.14 (2016-07-06):
    - fix preserve_quotes missing on original Loaders (as reported
      by Leynos, bitbucket issue 38)

  0.11.13 (2016-07-06):
    - documentation only, automated linux wheels

  0.11.12 (2016-07-06):
    - added support for roundtrip of single/double quoted scalars using:
      ruamel.yaml.round_trip_load(stream, preserve_quotes=True)

  0.11.0 (2016-02-18):
    - RoundTripLoader loads 1.2 by default (no sexagesimals, 012 octals nor
      yes/no/on/off booleans
