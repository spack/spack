============================================
The packages.spack.io Package Index REST API
============================================

This directory provides the docker recipe for the Spack package index on https://packages.spack.io

On each merge to ``develop``, DockerHub builds a new image ``spack/packages.spack.io`` which is configured in:
  https://cloud.docker.com/u/spack/repository/docker/spack/packages.spack.io/builds/edit

------------
The REST API
------------

The API is a simple, file-based JSON index.
A specific package can be queried via the URI syntax:
``https://packages.spack.io/api/:firstLetter/:packageName.json``
which will return a HTTP status code ``200`` with a JSON file for all valid packages (content from ``spack list --format version_json``) and HTTP status code ``404`` for all other package names.

Examples:

- https://packages.spack.io/api/a/adios2.json
- https://packages.spack.io/api/p/py-pandas.json

There is also the full index available at once under https://packages.spack.io/api/packages.json

Current down-stream dependencies are, e.g. the https://shields.io service:

- https://shields.io/category/version
- https://github.com/badges/shields/pull/3536

--------------------
Local Build and Test
--------------------

Execute in your local Spack source root directory:

.. code-block:: bash

   docker build -t spack/packages.spack.io:latest -f share/spack/docker/package-index/Dockerfile .

Startup a local HTTP server on http://localhost:8080 via:

.. code-block:: bash

   docker run -p 8080:80 spack/packages.spack.io:latest
