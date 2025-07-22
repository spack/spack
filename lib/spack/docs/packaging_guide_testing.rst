.. Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 0
   :width: 100%

   * - :doc:`1. Creation <packaging_guide_creation>`
     - :doc:`2. Build <packaging_guide_build>`
     - **3. Testing**
     - :doc:`4. Advanced <packaging_guide_advanced>`

======================================
Packaging Guide: testing installations
======================================

In this part of the packaging guide we will cover how to ensure your package builds correctly by adding tests to it.


.. _checking_an_installation:

------------------------
Checking an installation
------------------------

A package that *appears* to install successfully does not mean
it is actually installed correctly or will continue to work indefinitely.
There are a number of possible points of failure so Spack provides
features for checking the software along the way.

Failures can occur during and after the installation process. The
build may start but the software may not end up fully installed. The
installed software may not work at all or as expected. The software
may work after being installed but, due to changes on the system,
may stop working days, weeks, or months after being installed.

This section describes Spack's support for checks that can be performed
during and after its installation. The former checks are referred to as
``build-time tests`` and the latter as ``stand-alone (or smoke) tests``.

.. _build_time-tests:

^^^^^^^^^^^^^^^^
Build-time tests
^^^^^^^^^^^^^^^^

Spack infers the status of a build based on the contents of the install
prefix. Success is assumed if anything (e.g., a file or directory) is
written after ``install()`` completes. Otherwise, the build is assumed
to have failed. However, the presence of install prefix contents
is not a sufficient indicator of success so Spack supports the addition
of tests that can be performed during `spack install` processing.

Consider a simple autotools build using the following commands:

.. code-block:: console

   $ ./configure --prefix=/path/to/installation/prefix
   $ make
   $ make install

Standard Autotools and CMake do not write anything to the prefix from
the ``configure`` and ``make`` commands. Files are only written from
the ``make install`` after the build completes.

.. note::

   If you want to learn more about ``Autotools`` and ``CMake`` packages
   in Spack, refer to :ref:`AutotoolsPackage <autotoolspackage>` and
   :ref:`CMakePackage <cmakepackage>`, respectively.

What can you do to check that the build is progressing satisfactorily?
If there are specific files and/or directories expected of a successful
installation, you can add basic, fast ``sanity checks``. You can also add
checks to be performed after one or more installation phases.

.. note::

   Build-time tests are performed when the ``--test`` option is passed
   to ``spack install``.

.. warning::

   Build-time test failures result in a failed installation of the software.


.. _sanity-checks:

""""""""""""""""""""
Adding sanity checks
""""""""""""""""""""

Unfortunately, many builds of scientific software modify the installation
prefix **before** ``make install``. Builds like this can falsely report
success when an error occurs before the installation is complete. Simple
sanity checks can be used to identify files and/or directories that are
required of a successful installation. Spack checks for the presence of
the files and directories after ``install()`` runs.

If any of the listed files or directories are missing, then the build will
fail and the install prefix will be removed. If they all exist, then Spack
considers the build successful from a sanity check perspective and keeps
the prefix in place.

For example, the sanity checks for the ``reframe`` package below specify
that eight paths must exist within the installation prefix after the
``install`` method completes.

.. code-block:: python

   class Reframe(Package):
       ...

       # sanity check
       sanity_check_is_file = [join_path("bin", "reframe")]
       sanity_check_is_dir  = ["bin", "config", "docs", "reframe", "tutorials",
                               "unittests", "cscs-checks"]

When you run ``spack install`` with tests enabled, Spack will ensure that
a successfully installed package has the required files and/or directories.

For example, running:

.. code-block:: console

   $ spack install --test=root reframe

results in Spack checking that the installation created the following **file**:

* ``self.prefix.bin.reframe``

and the following **directories**:

* ``self.prefix.bin``
* ``self.prefix.config``
* ``self.prefix.docs``
* ``self.prefix.reframe``
* ``self.prefix.tutorials``
* ``self.prefix.unittests``
* ``self.prefix.cscs-checks``

If **any** of these paths are missing, then Spack considers the installation
to have failed.

.. note::

   You **MUST** use ``sanity_check_is_file`` to specify required
   files and ``sanity_check_is_dir`` for required directories.

.. _install_phase-tests:

"""""""""""""""""""""""""""""""
Adding installation phase tests
"""""""""""""""""""""""""""""""

Sometimes packages appear to build "correctly" only to have runtime
behavior issues discovered at a later stage, such as after a full
software stack relying on them has been built. Checks can be performed
at different phases of the package installation to possibly avoid
these types of problems. Some checks are built-in to different build
systems, while others will need to be added to the package.

Built-in installation phase tests are provided by packages inheriting
from select :ref:`build systems <build-systems>`, where naming conventions
are used to identify typical test identifiers for those systems. In
general, you won't need to add anything to your package to take advantage
of these tests if your software's build system complies with the convention;
otherwise, you'll want or need to override the post-phase method to perform
other checks.

.. list-table:: Built-in installation phase tests
   :header-rows: 1

   * - Build System Class
     - Post-Build Phase Method (Runs)
     - Post-Install Phase Method (Runs)
   * - :ref:`AutotoolsPackage <autotoolspackage>`
     - ``check`` (``make test``, ``make check``)
     - ``installcheck`` (``make installcheck``)
   * - :ref:`CachedCMakePackage <cachedcmakepackage>`
     - ``check`` (``make check``, ``make test``)
     - Not applicable
   * - :ref:`CMakePackage <cmakepackage>`
     - ``check`` (``make check``, ``make test``)
     - Not applicable
   * - :ref:`MakefilePackage <makefilepackage>`
     - ``check`` (``make test``, ``make check``)
     - ``installcheck`` (``make installcheck``)
   * - :ref:`MesonPackage <mesonpackage>`
     - ``check`` (``make test``, ``make check``)
     - Not applicable
   * - :ref:`PerlPackage <perlpackage>`
     - ``check`` (``make test``)
     - Not applicable
   * - :ref:`PythonPackage <pythonpackage>`
     - Not applicable
     - ``test_imports`` (module imports)
   * - :ref:`QMakePackage <qmakepackage>`
     - ``check`` (``make check``)
     - Not applicable
   * - :ref:`SConsPackage <sconspackage>`
     - ``build_test`` (must be overridden)
     - Not applicable
   * - :ref:`SIPPackage <sippackage>`
     - Not applicable
     - ``test_imports`` (module imports)
   * - :ref:`WafPackage <wafpackage>`
     - ``build_test`` (must be overridden)
     - ``install_test`` (must be overridden)

For example, the ``Libelf`` package inherits from ``AutotoolsPackage``
and its ``Makefile`` has a standard ``check`` target. So Spack will
automatically run ``make check`` after the ``build`` phase when it
is installed using the ``--test`` option, such as:

.. code-block:: console

   $ spack install --test=root libelf

In addition to overriding any built-in build system installation
phase tests, you can write your own install phase tests. You will
need to use two decorators for each phase test method:

* ``run_after``
* ``on_package_attributes``

The first decorator tells Spack when in the installation process to
run your test method installation process; namely *after* the provided
installation phase. The second decorator tells Spack to only run the
checks when the ``--test`` option is provided on the command line.

.. note::

   Be sure to place the directives above your test method in the order
   ``run_after`` *then* ``on_package_attributes``.

.. note::

   You also want to be sure the package supports the phase you use
   in the ``run_after`` directive. For example, ``PackageBase`` only
   supports the ``install`` phase while the ``AutotoolsPackage`` and
   ``MakefilePackage`` support both ``install`` and ``build`` phases.

Assuming both ``build`` and ``install`` phases are available to you,
you could add additional checks to be performed after each of those
phases based on the skeleton provided below.

.. code-block:: python

   class YourMakefilePackage(MakefilePackage):
       ...

       @run_after("build")
       @on_package_attributes(run_tests=True)
       def check_build(self):
            # Add your custom post-build phase tests
            pass

       @run_after("install")
       @on_package_attributes(run_tests=True)
       def check_install(self):
            # Add your custom post-install phase tests
            pass

.. note::

    You could also schedule work to be done **before** a given phase
    using the ``run_before`` decorator.

By way of a concrete example, the ``reframe`` package mentioned
previously has a simple installation phase check that runs the
installed executable. The check is implemented as follows:

.. code-block:: python

   class Reframe(Package):
       ...

       # check if we can run reframe
       @run_after("install")
       @on_package_attributes(run_tests=True)
       def check_list(self):
            with working_dir(self.stage.source_path):
                reframe = Executable(self.prefix.bin.reframe)
                reframe("-l")

""""""""""""""""""""""""""""""""
Checking build-time test results
""""""""""""""""""""""""""""""""

Checking the results of these tests after running ``spack install --test``
can be done by viewing the spec's ``install-time-test-log.txt`` file whose
location will depend on whether the spec installed successfully.

A successful installation results in the build and stage logs being copied
to the ``.spack`` subdirectory of the spec's prefix. For example,

.. code-block:: console

   $ spack install --test=root zlib@1.2.13
   ...
   [+] /home/user/spack/opt/spack/linux-rhel8-broadwell/gcc-10.3.1/zlib-1.2.13-tehu6cbsujufa2tb6pu3xvc6echjstv6
   $ cat /home/user/spack/opt/spack/linux-rhel8-broadwell/gcc-10.3.1/zlib-1.2.13-tehu6cbsujufa2tb6pu3xvc6echjstv6/.spack/install-time-test-log.txt

If the installation fails due to build-time test failures, then both logs will
be left in the build stage directory as illustrated below:

.. code-block:: console

   $ spack install --test=root zlib@1.2.13
   ...
   See build log for details:
     /var/tmp/user/spack-stage/spack-stage-zlib-1.2.13-lxfsivs4htfdewxe7hbi2b3tekj4make/spack-build-out.txt

   $ cat /var/tmp/user/spack-stage/spack-stage-zlib-1.2.13-lxfsivs4htfdewxe7hbi2b3tekj4make/install-time-test-log.txt


.. _cmd-spack-test:

^^^^^^^^^^^^^^^^^
Stand-alone tests
^^^^^^^^^^^^^^^^^

While build-time tests are integrated with the installation process, stand-alone
tests are expected to run days, weeks, even months after the software is
installed. The goal is to provide a mechanism for gaining confidence that
packages work as installed **and** *continue* to work as the underlying
software evolves. Packages can add and inherit stand-alone tests. The
``spack test`` command is used for stand-alone testing.

.. admonition:: Stand-alone test methods should complete within a few minutes.

    Execution speed is important since these tests are intended to quickly
    assess whether installed specs work on the system. Spack cannot spare
    resources for more extensive testing of packages included in CI stacks.

    Consequently, stand-alone tests should run relatively quickly -- as in
    on the order of at most a few minutes -- while testing at least key aspects
    of the installed software. Save more extensive testing for other tools.

Tests are defined in the package using methods with names beginning ``test_``.
This allows Spack to support multiple independent checks, or parts. Files
needed for testing, such as source, data, and expected outputs, may be saved
from the build and/or stored with the package in the repository. Regardless
of origin, these files are automatically copied to the spec's test stage
directory prior to execution of the test method(s). Spack also provides helper
functions to facilitate common processing.

.. tip::

    **The status of stand-alone tests can be used to guide follow-up testing efforts.**

    Passing stand-alone tests justifies performing more thorough testing, such
    as running extensive unit or regression tests or tests that run at scale,
    when available. These tests are outside of the scope of Spack packaging.

    Failing stand-alone tests indicate problems with the installation and,
    therefore, no reason to proceed with more resource-intensive tests until
    the failures have been investigated.

.. _configure-test-stage:

""""""""""""""""""""""""""""""""""""
Configuring the test stage directory
""""""""""""""""""""""""""""""""""""

Stand-alone tests utilize a test stage directory to build, run, and track
tests in the same way Spack uses a build stage directory to install software.
The default test stage root directory, ``$HOME/.spack/test``, is defined in
:ref:`config.yaml <config-yaml>`. This location is customizable by adding or
changing the ``test_stage`` path such that:

.. code-block:: yaml

   config:
     test_stage: /path/to/test/stage

Packages can use the ``self.test_suite.stage`` property to access the path.

.. admonition:: Each spec being tested has its own test stage directory.

   The ``config:test_stage`` option is the path to the root of a
   **test suite**'s stage directories.

   Other package properties that provide paths to spec-specific subdirectories
   and files are described in :ref:`accessing-files`.

.. _adding-standalone-tests:

""""""""""""""""""""""""
Adding stand-alone tests
""""""""""""""""""""""""

Test recipes are defined in the package using methods with names beginning
``test_``. This allows for the implementation of multiple independent tests.
Each method has access to the information Spack tracks on the package, such
as options, compilers, and dependencies, supporting the customization of tests
to the build. Standard Python ``assert`` statements and other error reporting
mechanisms can be used. These exceptions are automatically caught and reported
as test failures.

Each test method is an *implicit test part* named by the method. Its purpose
is the method's docstring. Providing a meaningful purpose for the test gives
context that can aid debugging. Spack outputs both the name and purpose at the
start of test execution so it's also important that the docstring/purpose be
brief.

.. tip::

    We recommend naming test methods so it is clear *what* is being tested.
    For example, if a test method is building and/or running an executable
    called ``example``, then call the method ``test_example``. This, together
    with a similarly meaningful test purpose, will aid test comprehension,
    debugging, and maintainability.

Stand-alone tests run in an environment that provides access to information
on the installed software, such as build options, dependencies, and compilers.
Build options and dependencies are accessed using the same spec checks used
by build recipes. Examples of checking :ref:`variant settings <variants>` and
:ref:`spec constraints <spec-objects>` can be found at the provided links.

.. admonition:: Spack automatically sets up the test stage directory and environment.

    Spack automatically creates the test stage directory and copies
    relevant files *prior to* running tests. It can also ensure build
    dependencies are available **if** necessary.

    The path to the test stage is configurable (see :ref:`configure-test-stage`).

    Files that Spack knows to copy are those saved from the build (see
    :ref:`cache_extra_test_sources`) and those added to the package repository
    (see :ref:`cache_custom_files`).

    Spack will use the value of the ``test_requires_compiler`` property to
    determine whether it needs to also set up build dependencies (see
    :ref:`test-build-tests`).

The ``MyPackage`` package below provides two basic test examples:
``test_example`` and ``test_example2``.  The first runs the installed
``example`` and ensures its output contains an expected string. The second
runs ``example2`` without checking output so is only concerned with confirming
the executable runs successfully. If the installed spec is not expected to have
``example2``, then the check at the top of the method will raise a special
``SkipTest`` exception, which is captured to facilitate reporting skipped test
parts to tools like CDash.

.. code-block:: python

   class MyPackage(Package):
       ...

       def test_example(self):
           """ensure installed example works"""
           expected = "Done."
           example = which(self.prefix.bin.example)

           # Capture stdout and stderr from running the Executable
           # and check that the expected output was produced.
           out = example(output=str.split, error=str.split)
           assert expected in out, f"Expected '{expected}' in the output"

       def test_example2(self):
           """run installed example2"""
           if self.spec.satisfies("@:1.0"):
               # Raise SkipTest to ensure flagging the test as skipped for
               # test reporting purposes.
               raise SkipTest("Test is only available for v1.1 on")

           example2 = which(self.prefix.bin.example2)
           example2()

Output showing the identification of each test part after running the tests
is illustrated below.

.. code-block:: console

   $ spack test run --alias mypackage mypackage@2.0
   ==> Spack test mypackage
   ...
   $ spack test results -l mypackage
   ==> Results for test suite 'mypackage':
   ...
   ==> [2024-03-10-16:03:56.625439] test: test_example: ensure installed example works
   ...
   PASSED: MyPackage::test_example
   ==> [2024-03-10-16:03:56.625439] test: test_example2: run installed example2
   ...
   PASSED: MyPackage::test_example2

.. admonition:: Do NOT implement tests that must run in the installation prefix.

   Use of the package spec's installation prefix for building and running
   tests is **strongly discouraged**. Doing so causes permission errors for
   shared spack instances *and* facilities that install the software in
   read-only file systems or directories.

   Instead, start these test methods by explicitly copying the needed files
   from the installation prefix to the test stage directory. Note the test
   stage directory is the current directory when the test is executed with
   the ``spack test run`` command.

.. admonition:: Test methods for library packages should build test executables.

   Stand-alone tests for library packages *should* build test executables
   that utilize the *installed* library. Doing so ensures the tests follow
   a similar build process that users of the library would follow.

   For more information on how to do this, see :ref:`test-build-tests`.

.. tip::

   If you want to see more examples from packages with stand-alone tests, run
   ``spack pkg grep "def\stest" | sed "s/\/package.py.*//g" | sort -u``
   from the command line to get a list of the packages.

.. _adding-standalone-test-parts:

"""""""""""""""""""""""""""""
Adding stand-alone test parts
"""""""""""""""""""""""""""""

Sometimes dependencies between steps of a test lend themselves to being
broken into parts. Tracking the pass/fail status of each part may aid
debugging. Spack provides a ``test_part`` context manager for use within
test methods.

Each test part is independently run, tracked, and reported. Test parts are
executed in the order they appear. If one fails, subsequent test parts are
still performed even if they would also fail. This allows tools like CDash
to track and report the status of test parts across runs. The pass/fail status
of the enclosing test is derived from the statuses of the embedded test parts.

.. admonition:: Test method and test part names **must** be unique.

   Test results reporting requires that test methods and embedded test parts
   within a package have unique names.

The signature for ``test_part`` is:

.. code-block:: python

   def test_part(pkg, test_name, purpose, work_dir=".", verbose=False):

where each argument has the following meaning:

* ``pkg`` is an instance of the package for the spec under test.

* ``test_name`` is the name of the test part, which must start with ``test_``.

* ``purpose`` is a brief description used as a heading for the test part.

  Output from the test is written to a test log file allowing the test name
  and purpose to be searched for test part confirmation and debugging.

* ``work_dir`` is the path to the directory in which the test will run.

  The default of ``None``, or ``"."``, corresponds to the spec's test
  stage (i.e., ``self.test_suite.test_dir_for_spec(self.spec)``).

.. admonition:: Start test part names with the name of the enclosing test.

   We **highly recommend** starting the names of test parts with the name
   of the enclosing test. Doing so helps with the comprehension, readability
   and debugging of test results.

Suppose ``MyPackage`` installs multiple executables that need to run in a
specific order since the outputs from one are inputs of others. Further suppose
we want to add an integration test that runs the executables in order. We can
accomplish this goal by implementing a stand-alone test method consisting of
test parts for each executable as follows:

.. code-block:: python

   class MyPackage(Package):
       ...

       def test_series(self):
           """run setup, perform, and report"""

           with test_part(self, "test_series_setup", purpose="setup operation"):
                exe = which(self.prefix.bin.setup))
                exe()

           with test_part(self, "test_series_run", purpose="perform operation"):
                exe = which(self.prefix.bin.run))
                exe()

           with test_part(self, "test_series_report", purpose="generate report"):
                exe = which(self.prefix.bin.report))
                exe()

The result is ``test_series`` runs the following executable in order: ``setup``,
``run``, and ``report``. In this case no options are passed to any of the
executables and no outputs from running them are checked. Consequently, the
implementation could be simplified with a for-loop as follows:

.. code-block:: python

   class MyPackage(Package):
       ...

       def test_series(self):
           """execute series setup, run, and report"""

           for exe, reason in [
               ("setup", "setup operation"),
               ("run", "perform operation"),
               ("report", "generate report")
           ]:
               with test_part(self, f"test_series_{exe}", purpose=reason):
                   exe = which(self.prefix.bin.join(exe))
                   exe()

In both cases, since we're using a context manager, each test part in
``test_series`` will execute regardless of the status of the other test
parts.

Now let's look at the output from running the stand-alone tests where
the second test part, ``test_series_run``, fails.

.. code-block:: console

   $ spack test run --alias mypackage mypackage@1.0
   ==> Spack test mypackage
   ...
   $ spack test results -l mypackage
   ==> Results for test suite 'mypackage':
   ...
   ==> [2024-03-10-16:03:56.625204] test: test_series: execute series setup, run, and report
   ==> [2024-03-10-16:03:56.625439] test: test_series_setup: setup operation
   ...
   PASSED: MyPackage::test_series_setup
   ==> [2024-03-10-16:03:56.625555] test: test_series_run: perform operation
   ...
   FAILED: MyPackage::test_series_run
   ==> [2024-03-10-16:03:57.003456] test: test_series_report: generate report
   ...
   FAILED: MyPackage::test_series_report
   FAILED: MyPackage::test_series
   ...

Since test parts depended on the success of previous parts, we see that the
failure of one results in the failure of subsequent checks and the overall
result of the test method, ``test_series``, is failure.

.. tip::

   If you want to see more examples from packages using ``test_part``, run
   ``spack pkg grep "test_part(" | sed "s/\/package.py.*//g" | sort -u``
   from the command line to get a list of the packages.

.. _test-build-tests:

"""""""""""""""""""""""""""""""""""""
Building and running test executables
"""""""""""""""""""""""""""""""""""""

.. admonition:: Reuse build-time sources and (small) input data sets when possible.

    We **highly recommend** reusing build-time test sources and pared down
    input files for testing installed software. These files are easier
    to keep synchronized with software capabilities when they reside
    within the software's repository. More information on saving files from
    the installation process can be found at :ref:`cache_extra_test_sources`.

    If that is not possible, you can add test-related files to the package
    repository (see :ref:`cache_custom_files`). It will be important to
    remember to maintain them so they work across listed or supported versions
    of the package.

Packages that build libraries are good examples of cases where you'll want
to build test executables from the installed software before running them.
Doing so requires you to let Spack know it needs to load the package's
compiler configuration. This is accomplished by setting the package's
``test_requires_compiler`` property to ``True``.

.. admonition:: ``test_requires_compiler = True`` is required to build test executables.

   Setting the property to ``True`` ensures access to the compiler through
   canonical environment variables (e.g., ``CC``, ``CXX``, ``FC``, ``F77``).
   It also gives access to build dependencies like ``cmake`` through their
   ``spec objects`` (e.g., ``self.spec["cmake"].prefix.bin.cmake`` for the
   path or ``self.spec["cmake"].command`` for the ``Executable`` instance).

   Be sure to add the property at the top of the package class under other
   properties like the ``homepage``.

The example below, which ignores how ``cxx-example.cpp`` is acquired,
illustrates the basic process of compiling a test executable using the
installed library before running it.

.. code-block:: python

   class MyLibrary(Package):
       ...

       test_requires_compiler = True
       ...

       def test_cxx_example(self):
           """build and run cxx-example"""
           exe = "cxx-example"
           ...
           cxx = which(os.environ["CXX"])
           cxx(
               f"-L{self.prefix.lib}",
               f"-I{self.prefix.include}",
               f"{exe}.cpp",
               "-o", exe
           )
           cxx_example = which(exe)
           cxx_example()

Typically the files used to build and/or run test executables are either
cached from the installation (see :ref:`cache_extra_test_sources`) or added
to the package repository (see :ref:`cache_custom_files`). There is nothing
preventing the use of both.

.. _cache_extra_test_sources:

""""""""""""""""""""""""""""""""""""
Saving build- and install-time files
""""""""""""""""""""""""""""""""""""

You can use the ``cache_extra_test_sources`` helper routine to copy
directories and/or files from the source build stage directory to the
package's installation directory. Spack will automatically copy these
files for you when it sets up the test stage directory and before it
begins running the tests.

The signature for ``cache_extra_test_sources`` is:

.. code-block:: python

   def cache_extra_test_sources(pkg, srcs):

where each argument has the following meaning:

* ``pkg`` is an instance of the package for the spec under test.

* ``srcs`` is a string *or* a list of strings corresponding to the
  paths of subdirectories and/or files needed for stand-alone testing.

.. warning::

   Paths provided in the ``srcs`` argument **must be relative** to the
   staged source directory. They will be copied to the equivalent relative
   location under the test stage directory prior to test execution.

Contents of subdirectories and files are copied to a special test cache
subdirectory of the installation prefix. They are automatically copied to
the appropriate relative paths under the test stage directory prior to
executing stand-alone tests.

.. tip::

    *Perform test-related conversions once when copying files.*

    If one or more of the copied files needs to be modified to reference
    the installed software, it is recommended that those changes be made
    to the cached files **once** in the post-``install`` copy method
    **after** the call to ``cache_extra_test_sources``. This will reduce
    the amount of unnecessary work in the test method **and** avoid problems
    running stand-alone tests in shared instances and facility deployments.

    The ``filter_file`` function can be quite useful for such changes
    (see :ref:`file-filtering`).

Below is a basic example of a test that relies on files from the installation.
This package method reuses the contents of the ``examples`` subdirectory,
which is assumed to have all of the files necessary to allow ``make`` to
compile and link ``foo.c`` and ``bar.c`` against the package's installed
library.

.. code-block:: python

   class MyLibPackage(MakefilePackage):
       ...

       @run_after("install")
       def copy_test_files(self):
           cache_extra_test_sources(self, "examples")

       def test_example(self):
           """build and run the examples"""
           examples_dir = self.test_suite.current_test_cache_dir.examples
           with working_dir(examples_dir):
               make = which("make")
               make()

               for program in ["foo", "bar"]:
                   with test_part(
                       self,
                       f"test_example_{program}",
                       purpose=f"ensure {program} runs"
                   ):
                       exe = Executable(program)
                       exe()

In this case, ``copy_test_files`` copies the associated files from the
build stage to the package's test cache directory under the installation
prefix. Running ``spack test run`` for the package results in Spack copying
the directory and its contents to the test stage directory. The
``working_dir`` context manager ensures the commands within it are executed
from the ``examples_dir``. The test builds the software using ``make`` before
running each executable, ``foo`` and ``bar``, as independent test parts.

.. note::

   The method name ``copy_test_files`` here is for illustration purposes.
   You are free to use a name that is better suited to your package.

   The key to copying files for stand-alone testing at build time is use
   of the ``run_after`` directive, which ensures the associated files are
   copied **after** the provided build stage (``install``) when the installation
   prefix **and** files are available.

   The test method uses the path contained in the package's
   ``self.test_suite.current_test_cache_dir`` property for the root directory
   of the copied files. In this case, that's the ``examples`` subdirectory.

.. tip::

   If you want to see more examples from packages that cache build files, run
   ``spack pkg grep cache_extra_test_sources | sed "s/\/package.py.*//g" | sort -u``
   from the command line to get a list of the packages.

.. _cache_custom_files:

"""""""""""""""""""
Adding custom files
"""""""""""""""""""

Sometimes it is helpful or necessary to include custom files for building and/or
checking the results of tests as part of the package. Examples of the types
of files that might be useful are:

- test source files
- test input files
- test build scripts
- expected test outputs

While obtaining such files from the software repository is preferred (see
:ref:`cache_extra_test_sources`), there are circumstances where doing so is not
feasible such as when the software is not being actively maintained. When test
files cannot be obtained from the repository or there is a need to supplement
files that can, Spack supports the inclusion of additional files under the
``test`` subdirectory of the package in the Spack repository.

The following example assumes a ``custom-example.c`` is saved in ``MyLibrary``
package's ``test`` subdirectory. It also assumes the program simply needs to
be compiled and linked against the installed ``MyLibrary`` software.

.. code-block:: python

   class MyLibrary(Package):
       ...

       test_requires_compiler = True
       ...

       def test_custom_example(self):
           """build and run custom-example"""
           src_dir = self.test_suite.current_test_data_dir
           exe = "custom-example"

           with working_dir(src_dir):
               cc = which(os.environ["CC"])
               cc(
                   f"-L{self.prefix.lib}",
                   f"-I{self.prefix.include}",
                   f"{exe}.cpp",
                   "-o", exe
               )

               custom_example = Executable(exe)
               custom_example()

In this case, ``spack test run`` for the package results in Spack copying
the contents of the ``test`` subdirectory to the test stage directory path
in ``self.test_suite.current_test_data_dir`` before calling
``test_custom_example``. Use of the ``working_dir`` context manager
ensures the commands to build and run the program are performed from
within the appropriate subdirectory of the test stage.

.. _expected_test_output_from_file:

"""""""""""""""""""""""""""""""""""
Reading expected output from a file
"""""""""""""""""""""""""""""""""""

The helper function ``get_escaped_text_output`` is available for packages
to retrieve properly formatted text from a file potentially containing
special characters.

The signature for ``get_escaped_text_output`` is:

.. code-block:: python

   def get_escaped_text_output(filename):

where ``filename`` is the path to the file containing the expected output.

The path provided to ``filename`` for one of the copied custom files
(:ref:`custom file <cache_custom_files>`) is in the path rooted at
``self.test_suite.current_test_data_dir``.

The example below shows how to reference both the custom database
(``packages.db``) and expected output (``dump.out``) files Spack copies
to the test stage:

.. code-block:: python

   import re

   class Sqlite(AutotoolsPackage):
       ...

       def test_example(self):
           """check example table dump"""
           test_data_dir = self.test_suite.current_test_data_dir
           db_filename = test_data_dir.join("packages.db")
           ..
           expected = get_escaped_text_output(test_data_dir.join("dump.out"))
           sqlite3 = which(self.prefix.bin.sqlite3)
           out = sqlite3(
               db_filename, ".dump", output=str.split, error=str.split
           )
           for exp in expected:
               assert re.search(exp, out), f"Expected '{exp}' in output"

If the files were instead cached from installing the software, the paths to the
two files would be found under the ``self.test_suite.current_test_cache_dir``
directory as shown below:

.. code-block:: python

       def test_example(self):
           """check example table dump"""
           test_cache_dir = self.test_suite.current_test_cache_dir
           db_filename = test_cache_dir.join("packages.db")
           ..
           expected = get_escaped_text_output(test_cache_dir.join("dump.out"))
           ...

Alternatively, if both files had been installed by the software into the
``share/tests`` subdirectory of the installation prefix, the paths to the
two files would be referenced as follows:

.. code-block:: python

       def test_example(self):
           """check example table dump"""
           db_filename = self.prefix.share.tests.join("packages.db")
           ..
           expected = get_escaped_text_output(
               self.prefix.share.tests.join("dump.out")
           )
           ...

.. _check_outputs:

""""""""""""""""""""""""""""""""""""
Comparing expected to actual outputs
""""""""""""""""""""""""""""""""""""

The ``check_outputs`` helper routine is available for packages to ensure
multiple expected outputs from running an executable are contained within
the actual outputs.

The signature for ``check_outputs`` is:

.. code-block:: python

   def check_outputs(expected, actual):

where each argument has the expected type and meaning:

* ``expected`` is a string or list of strings containing the expected (raw)
  output.

* ``actual`` is a string containing the actual output from executing the command.

Invoking the method is the equivalent of:

.. code-block:: python

   errors = []
   for check in expected:
       if not re.search(check, actual):
           errors.append(f"Expected '{check}' in output '{actual}'")
   if errors:
       raise RuntimeError("\n ".join(errors))

.. tip::

   If you want to see more examples from packages that use this helper, run
   ``spack pkg grep check_outputs | sed "s/\/package.py.*//g" | sort -u``
   from the command line to get a list of the packages.


.. _accessing-files:

"""""""""""""""""""""""""""""""""""""""""
Finding package- and test-related files
"""""""""""""""""""""""""""""""""""""""""

You may need to access files from one or more locations when writing
stand-alone tests. This can happen if the software's repository does not
include test source files or includes them but has no way to build the
executables using the installed headers and libraries. In these cases
you may need to reference the files relative to one or more root directories.
The table below lists relevant path properties and provides additional
examples of their use. See :ref:`expected_test_output_from_file` for
examples of accessing files saved from the software repository, package
repository, and installation.

.. list-table:: Directory-to-property mapping
   :header-rows: 1

   * - Root Directory
     - Package Property
     - Example(s)
   * - Package (Spec) Installation
     - ``self.prefix``
     - ``self.prefix.include``, ``self.prefix.lib``
   * - Dependency Installation
     - ``self.spec["<dependency-package>"].prefix``
     - ``self.spec["trilinos"].prefix.include``
   * - Test Suite Stage
     - ``self.test_suite.stage``
     - ``join_path(self.test_suite.stage, "results.txt")``
   * - Spec's Test Stage
     - ``self.test_suite.test_dir_for_spec(<spec>)``
     - ``self.test_suite.test_dir_for_spec(self.spec)``
   * - Current Spec's Build-time Files
     - ``self.test_suite.current_test_cache_dir``
     - ``join_path(self.test_suite.current_test_cache_dir.examples, "foo.c")``
   * - Current Spec's Custom Test Files
     - ``self.test_suite.current_test_data_dir``
     - ``join_path(self.test_suite.current_test_data_dir, "hello.f90")``

.. _inheriting-tests:

""""""""""""""""""""""""""""
Inheriting stand-alone tests
""""""""""""""""""""""""""""

Stand-alone tests defined in parent (e.g., :ref:`build-systems`) and
virtual (e.g., :ref:`virtual-dependencies`) packages are executed by
packages that inherit from or provide interface implementations for those
packages, respectively.

The table below summarizes the stand-alone tests that will be executed along
with those implemented in the package itself.

.. list-table:: Inherited/provided stand-alone tests
   :header-rows: 1

   * - Parent/Provider Package
     - Stand-alone Tests
   * - `C
       <https://github.com/spack/spack-packages/blob/develop/repos/spack_repo/builtin/packages/c>`_
     - Compiles ``hello.c`` and runs it
   * - `Cxx
       <https://github.com/spack/spack-packages/blob/develop/repos/spack_repo/builtin/packages/cxx>`_
     - Compiles and runs several ``hello`` programs
   * - `Fortran
       <https://github.com/spack/spack-packages/blob/develop/repos/spack_repo/builtin/packages/fortran>`_
     - Compiles and runs ``hello`` programs (``F`` and ``f90``)
   * - `Mpi
       <https://github.com/spack/spack-packages/blob/develop/repos/spack_repo/builtin/packages/mpi>`_
     - Compiles and runs ``mpi_hello`` (``c``, ``fortran``)
   * - :ref:`PythonPackage <pythonpackage>`
     - Imports modules listed in the ``self.import_modules`` property with defaults derived from the tarball
   * - :ref:`SipPackage <sippackage>`
     - Imports modules listed in the ``self.import_modules`` property with defaults derived from the tarball

These tests are very basic so it is important that package developers and
maintainers provide additional stand-alone tests customized to the package.

.. warning::

   Any package that implements a test method with the same name as an
   inherited method will override the inherited method. If that is not the
   goal and you are not explicitly calling and adding functionality to
   the inherited method for the test, then make sure that all test methods
   and embedded test parts have unique test names.

One example of a package that adds its own stand-alone tests to those
"inherited" by the virtual package it provides an implementation for is
the `OpenMPI package
<https://github.com/spack/spack-packages/blob/develop/repos/spack_repo/builtin/packages/openmpi/package.py>`_.

Below are snippets from running and viewing the stand-alone test results
for ``openmpi``:

.. code-block:: console

   $ spack test run --alias openmpi openmpi@4.1.4
   ==> Spack test openmpi
   ==> Testing package openmpi-4.1.4-ubmrigj
   ============================== 1 passed of 1 spec ==============================

   $ spack test results -l openmpi
   ==> Results for test suite 'openmpi':
   ==> test specs:
   ==>   openmpi-4.1.4-ubmrigj PASSED
   ==> Testing package openmpi-4.1.4-ubmrigj
   ==> [2023-03-10-16:03:56.160361] Installing $spack/opt/spack/linux-rhel7-broadwell/gcc-8.3.1/openmpi-4.1.4-ubmrigjrqcafh3hffqcx7yz2nc5jstra/.spack/test to $test_stage/xez37ekynfbi4e7h4zdndfemzufftnym/openmpi-4.1.4-ubmrigj/cache/openmpi
   ==> [2023-03-10-16:03:56.625204] test: test_bin: test installed binaries
   ==> [2023-03-10-16:03:56.625439] test: test_bin_mpirun: run and check output of mpirun
   ==> [2023-03-10-16:03:56.629807] '$spack/opt/spack/linux-rhel7-broadwell/gcc-8.3.1/openmpi-4.1.4-ubmrigjrqcafh3hffqcx7yz2nc5jstra/bin/mpirun' '-n' '1' 'ls' '..'
   openmpi-4.1.4-ubmrigj            repo
   openmpi-4.1.4-ubmrigj-test-out.txt  test_suite.lock
   PASSED: test_bin_mpirun
   ...
   ==> [2023-03-10-16:04:01.486977] test: test_version_oshcc: ensure version of oshcc is 8.3.1
   SKIPPED: test_version_oshcc: oshcc is not installed
   ...
   ==> [2023-03-10-16:04:02.215227] Completed testing
   ==> [2023-03-10-16:04:02.215597]
   ======================== SUMMARY: openmpi-4.1.4-ubmrigj ========================
   Openmpi::test_bin_mpirun .. PASSED
   Openmpi::test_bin_ompi_info .. PASSED
   Openmpi::test_bin_oshmem_info .. SKIPPED
   Openmpi::test_bin_oshrun .. SKIPPED
   Openmpi::test_bin_shmemrun .. SKIPPED
   Openmpi::test_bin .. PASSED
   ...
   ============================== 1 passed of 1 spec ==============================


.. _cmd-spack-test-list:

"""""""""""""""""""
``spack test list``
"""""""""""""""""""

Packages available for install testing can be found using the
``spack test list`` command. The command outputs all installed
packages that have defined stand-alone test methods.

Alternatively you can use the ``--all`` option to get a list of
all packages that have stand-alone test methods even if the packages
are not installed.

For more information, refer to `spack test list
<https://spack.readthedocs.io/en/latest/command_index.html#spack-test-list>`_.

.. _cmd-spack-test-run:

""""""""""""""""""
``spack test run``
""""""""""""""""""

Install tests can be run for one or more installed packages using
the ``spack test run`` command. A ``test suite`` is created for all
of the provided specs. The command accepts the same arguments provided
to ``spack install`` (see :ref:`sec-specs`). If no specs are provided
the command tests all specs in the active environment or all specs
installed in the Spack instance if no environment is active.

Test suites can be named using the ``--alias`` option. Unaliased
test suites use the content hash of their specs as their name.

Some of the more commonly used debugging options are:

- ``--fail-fast`` stops testing each package after the first failure
- ``--fail-first`` stops testing packages after the first failure

Test output is written to a text log file by default, though ``junit``
and ``cdash`` are outputs available through the ``--log-format`` option.

For more information, refer to `spack test run
<https://spack.readthedocs.io/en/latest/command_index.html#spack-test-run>`_.


.. _cmd-spack-test-results:

""""""""""""""""""""""
``spack test results``
""""""""""""""""""""""

The ``spack test results`` command shows results for all completed
test suites by default. The alias or content hash can be provided to
limit reporting to the corresponding test suite.

The ``--logs`` option includes the output generated by the associated
test(s) to facilitate debugging.

The ``--failed`` option limits results shown to that of the failed
tests, if any, of matching packages.

For more information, refer to `spack test results
<https://spack.readthedocs.io/en/latest/command_index.html#spack-test-results>`_.

.. _cmd-spack-test-find:

"""""""""""""""""""
``spack test find``
"""""""""""""""""""

The ``spack test find`` command lists the aliases or content hashes
of all test suites whose results are available.

For more information, refer to `spack test find
<https://spack.readthedocs.io/en/latest/command_index.html#spack-test-find>`_.

.. _cmd-spack-test-remove:

"""""""""""""""""""""
``spack test remove``
"""""""""""""""""""""

The ``spack test remove`` command removes test suites to declutter
the test stage directory. You are prompted to confirm the removal
of each test suite **unless** you use the ``--yes-to-all`` option.

For more information, refer to `spack test remove
<https://spack.readthedocs.io/en/latest/command_index.html#spack-test-remove>`_.
