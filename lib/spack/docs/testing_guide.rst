.. _testing-guide:

=============
Testing Guide
=============

This guide is intended for developers or administrators who want to
integrate or test software releases built with Spack.

---------
Reporting
---------
The install and testing infrastructure of Spack supports multiple output formats for
reporting the result of package builds in tools such as Jenkins or CDash.

The output formats can be enabled by e.g.

.. code-block:: console

   $ spack install --log-format=junit <spec>

Per default the log results will be placed into `var/<format>/test-<short_spec>.xml`.
To change the default behaviour, use

.. code-block:: console

   $ spack install --log-file report --log-format=junit <spec>

The logs contain one test case per package being built.


^^^^^
Junit
^^^^^

With 

.. code-block:: console

   $ spack install --log-format=junit <spec>

Spack creates files in `junit` format.


^^^^^
CDash
^^^^^

Spack supports the XML format used by `CDash <http://www.cdash.org/>`_.
To create reports in this format, do

.. code-block:: console

   $ spack install --log-file report --log-format=cdash <spec>

This will produce each one file for the configure, build, and test step.
For spack only the test step is relevant, as the build of each package is 
considered a test case. The CDash `build name` is the spec provided at command 
line.

To upload the reports to an existing CDash instance, you can use the tool `curl`:

.. code-block:: console

   $ curl --upload-file report.build.xml <cdash url>/submit.php?project=<projectname>
   $ curl --upload-file report.configure.xml <cdash url>/submit.php?project=<projectname>
   $ curl --upload-file report.test.xml <cdash url>/submit.php?project=<projectname>
