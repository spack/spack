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



----------------
using test-suite
----------------

Test-suite is designed to read in a yaml file describing all packages and compilers along 
with versions. Using the enabled field will allow you to focus on specific packages.
To narrow down the scope of a package or compiler, you can use the exclusion field.

--Example of a yaml file---

enable: [bzip2, libelf, .. ,libdwarf]

exclusions: []

packages:
  - abinit:
    - versions: [8.0.8b]
  - ack:
    - versions: [2.14]

  compilers:
  - gcc:
    - versions: [4.9.0, ... 4.7.1, 4.6.3, 4.6.1]
  - clang:
    - versions: [7.3.0, 3.4, ... 3.1]
  
dashboard: ["https://spack.io/cdash/submit.php?project=spack"]

path: "~/home/username"

---exclusion examples---
 	pkg%compiler
    pkg@version
    compiler@version
    pkg@version%compiler@version
    pkg@version%compiler
    pkg%compiler@version
    pkg
    compiler

Test-suite provides two outputs. One being a simple cdash output that only contains the build output.
Complete contains all stages, configure, build and test. Using the -c or --complete flag will change the output mode.
Test-suite produces simple by default.

To run test-suite: 
	$ spack test-suite -c /location/of/yamlFile

Currently output files are stored in /spack/var/spack/cdash this may change in the future.
If a dashboard field is provided the cdash output will be sent via PUT request, otherwise files will be left in /spack/var/spack/cdash.

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


