.. _testing-guide:

=======
Testing
=======

This guide is intended for developers or administrators who want to
integrate or test software releases built with Spack.

.. _test-single-build:

-------------------------
Testing a single build
-------------------------

Spack's :ref:`install <cmd-spack-install>` command can run a spack build
as a test and generate output for web dashboards such as `CDash
<http://www.cdash.org/>`_, `Jenkins <https://jenkins.io/>`_, or `Bamboo
<https://www.atlassian.com/software/bamboo>`_.

These output formats are enabled using the ``--log-format`` option to
``spack install``:

.. code-block:: console

   $ spack install --log-format=junit <spec>

By default, the log results will be placed into
``var/<format>/test-<short_spec>.xml``.  To change the default behaviour,
use

.. code-block:: console

   $ spack install --log-file report --log-format=junit <spec>

The logs contain one test case per package being built.

^^^^^
Junit
^^^^^

To generate logs in `JUnit <http://junit.org/>`_ format, use
``--log-format=junit``:

.. code-block:: console

   $ spack install --log-format=junit <spec>

The `Jenkins <https://jenkins.io/>`_, `Bamboo
<https://www.atlassian.com/software/bamboo>`_ and many other tools can
use JUnit.

^^^^^
CDash
^^^^^

`CDash <https://www.cdash.org>`_ is an open source web application from
`Kitware <https://www.kitware.com>`_ that displays the results of
software builds and test runs.  Spack can generate output for CDash using
either of these options to ``spack install``:

  * ``--log-format=cdash-simple``
  * ``--log-format=cdash-complete``

For example:

.. code-block:: console

   $ spack install --log-file report --log-format=cdash-simple libelf

This will generate a file called ``report.xml`` that contains a
description of a build of ``libelf``:

.. code-block:: xml

    <?xml version="1.0" ?>
    <Site BuildName="libelf@0.8.12%gcc@6.2.0 arch darwin-elcapitan-x86_64 /qmbmcez"
          BuildStamp="20172803-12:00:08-Experimental"
          CompilerName="gcc"
          CompilerVersion="6.2.0"
          Hostname="OS X 10.11.6"
          Name="atala.llnl.gov"
          OSName="OS X 10.11.6">
        <Build>
            <StartDateTime>Mar 28 12:00 PDT</StartDateTime>
            <StartBuildTime>1490727615</StartBuildTime>
            <BuildCommand>spack install</BuildCommand>
            <Log Encoding="base64">
                <!-- ... long build log text goes here ... -->
            </Log>
            <EndDateTime>Mar 28 12:00 PDT</EndDateTime>
            <EndBuildTime>1490727615</EndBuildTime>
            <ElapsedMinutes>0</ElapsedMinutes>
        </Build>
    </Site>

Spack uses a short version of each package's spec as the CDash build
name, which will be shown in the dashboard.

For more detailed output, you can use the ``cdash-complete`` format:

.. code-block:: console

   $ spack install --log-file report --log-format=cdash-complete libelf

This will create separate files: ``report.build.xml``,
``report.configure.xml``, and ``report.test.xml``, for the build,
configure, and tests steps, respectively.

If you want to upload these fils to a CDash instance, you can use ``curl``:

.. code-block:: console

   $ curl --upload-file report.build.xml https://example.com/cdash/submit.php?project=<projectname>
   $ curl --upload-file report.configure.xml https://example.com/cdash/submit.php?project=<projectname>
   $ curl --upload-file report.test.xml https://example.com/cdash/submit.php?project=<projectname>

Spack can also automate this step for you as part of the ``spack
test-suite`` command described in the next section.


.. _cmd-spack-test-suite:

---------------------
CDash test suites
---------------------

The ``spack test-suite`` command reads in a specialy formatted YAML file
describing a set of combinatorial tests.  It can be used to easily test a
package or suite of packages with many different compilers and build
options.

^^^^^^^^^^^^^^^^^^^^^^^^^^^
Test suite YAML format
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here's an example file:

.. code-block:: yaml

   #
   # This YAML file describes a Spack test suite
   #
   test-suite:
       #
       # Optional include/exclude spec lists.
       #

       # Only specs that match a spec in this list will be included in
       # the tests.  If include is missing, all specs are built.
       [bzip2, libelf, libdwarf]

       # Specs that match a spec in this list are excluded.
       # If exclude is missing or empty, all included packages are built.
       exclude: []

       #
       # List of packages, each with a set of versions to test.
       #
       packages:
         abinit:
           versions: [8.0.8b]
         ack:
           versions: [2.14]

       #
       # List of compiler versions. Each package is tested with all
       # compiler versions.
       #
       compilers:
       - gcc:
           - versions: [4.9.0, 4.7.1, 4.6.3, 4.6.1]
       - clang:
           - versions: [7.3.0, 3.4, 3.1]

       #
       # URL of the cdash server where results should be submitted.
       # Optional. Defaults to https://spack.io/cdash
       #
       cdash: ["https://spack.io/cdash"]

       #
       # Project on the cdash server where results should be submitted.
       # Optional. Defaults to 'spack'.
       #
       project: spack


All fields *except* ``packages`` and ``compilers`` are optional.  The
``packages`` section contains a list of Spack package names and versions
to be built.  Similarly, the ``compilers`` section contains a list of
compilers to test all the packages with.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Excluding and including builds
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can exclude or include builds that match a particular pattern using
lists of :ref:`Specs <sec-specs>`.  For example, to include only builds
of abinit, you could write:

.. code-block:: yaml

   include: [abinit]

To include only builds using some version of gcc, youc could write:

.. code-block:: yaml

   include: ['%gcc']

To add to that and exclude all builds of gcc 4.6, you could write:

.. code-block:: yaml

   include: ['%gcc']
   exclude: ['%gcc@4.6']

For more information on spec matching semantics, see the section on
:ref:`Specs <sec-specs>`.

.. note::

   Currently, we only support combinatorial builds with different package
   and compiler versions.  We are working on adding combinatorial builds
   on variants, compiler flags, and other spec attributes.


^^^^^^^^^^^^^
Build output
^^^^^^^^^^^^^

By default, ``spack test-suite`` creates output in a directory called
``spack-test-YYYY-MM-DD``, where ``YYYY-MM-DD`` is the date on which the
test suite was run.  For example, consider this ``test.yaml`` file:

.. code-block:: yaml

   test-suite:
     packages:
       libelf:
         versions: [0.8.12]
       libdwarf:
         versions: [0.8.12]

     compilers:
       clang:
         versions: [7.0.2-apple]
       gcc:
         versions: [6.2.0]

Running spack test-suite with this file would produce an output directory
called, e.g., ``spack-test-2017-03-28``:

.. code-block:: console

   $ spack test-suite ./test.yaml

   # ... output ...

   $ ls spack-test-2017-03-28
   build-libdwarf-0.8.12-5akzclxk74z44zml43yx767ipxd7wwz4.xml
   build-libdwarf-0.8.12-e2viv23cr6lih2gn4ap6327qdsz4boyn.xml
   build-libelf-0.8.12-qmbmcezdqmbwreie3u2cns5zwxvjmzil.xml
   build-libelf-0.8.12-yroox5qmqvpbrve6bgggxfyyekijundb.xml

These XML files are like the ones described in :ref:`test-single-build`,
but now there is a file for each parameter combination from the
``test.yaml`` file.  There are two builds each of ``libelf`` and
``libdwarf``, one for each compiler version.

``spack test-suite`` produces simple output by default.  To get the CDash
complete output (whcih shows separate configure, build, and test
results), use ``--complete`` flag to change the output mode:

.. code-block:: console

  $ spack test-suite --complete ./test.yaml

^^^^^^^^^^^^^^^^^^
Uploading results
^^^^^^^^^^^^^^^^^^

In addition to writing XML output to a local directory, ``spack
test-suite`` can automatically upload build results to a CDash server.

Results will be uploaded if you provide any of these parameters to
``spack test-suite``:

  * ``--cdash URL`` The URL of a CDash server to which we should upload
    files.  This defaults to ``https://spack.io/cdash``.

  * ``--project NAME`` The name of a project on the CDash server where
    the results should be reported.  This defaults to ``spack``.

If either of these options is provided, Spack uploads all test results to
the server.  For example, this command:

.. code-block:: console

   $ spack test-suite --cdash https://my.cdash.org --project myproject ./test.yaml

will run the test suite described by ``test.yaml`` and upload the results
to ``https://my.cdash.org/submit.php?project=myproject``.
