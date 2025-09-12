.. Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. meta::
   :description lang=en:
      Advanced topics in Spack packaging, covering packages with multiple build systems, making packages discoverable with spack external find, and specifying ABI compatibility.

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 0
   :width: 100%

   * - :doc:`1. Creation <packaging_guide_creation>`
     - :doc:`2. Build <packaging_guide_build>`
     - :doc:`3. Testing <packaging_guide_testing>`
     - **4. Advanced**

Packaging Guide: advanced topics
================================

This section of the packaging guide covers a few advanced topics.

.. _multiple_build_systems:

Multiple build systems
----------------------

It is not uncommon for a package to use different build systems across different versions or platforms.
For instance, a project might migrate from Autotools to CMake, or use a different build system on Windows than on UNIX.
Spack is designed to handle this seamlessly within a single ``package.py`` file.
While Spack uses one package class per recipe, it can manage multiple build systems by associating different *builder* classes with the package.
This design makes supporting multiple build systems straightforward and maintainable.

The following changes are needed to support multiple build systems in a package:

1. The package class should derive from *multiple base classes*, such as ``CMakePackage`` and ``AutotoolsPackage``.
2. The ``build_system`` directive is used to declare the available build systems and specify the default one.
3. The :doc:`build instructions <packaging_guide_build>` are specified in *separate builder classes*.

Here is a simple example of a package that supports both CMake and Autotools:

.. code-block:: python

   from spack.package import *
   from spack_repo.builtin.build_systems import cmake, autotools


   class Example(cmake.CMakePackage, autotools.AutotoolsPackage):
       variant("my_feature", default=True)
       build_system("cmake", "autotools", default="cmake")


   class CMakeBuilder(cmake.CMakeBuilder):
       def cmake_args(self):
           return [self.define_from_variant("MY_FEATURE", "my_feature")]


   class AutotoolsBuilder(autotools.AutotoolsBuilder):
       def configure_args(self):
           return self.with_or_without("my-feature", variant="my_feature")

When defining a package like this, Spack automatically makes the ``build_system`` **variant** available, which can be used to pick the desired build system at install time.
For example

.. code-block:: spec

   $ spack install example +feature build_system=cmake

makes Spack pick the ``CMakeBuilder`` class and runs ``cmake -DMY_FEATURE:BOOL=ON``.

Similarly

.. code-block:: spec

   $ spack install example +feature build_system=autotools

will pick the ``AutotoolsBuilder`` class and runs ``./configure --with-my-feature``.

With multiple build systems, we have a clear split between the :doc:`package metadata <packaging_guide_creation>` and the :doc:`build instructions <packaging_guide_build>`.
The directives such as ``depends_on``, ``variant``, ``patch`` go into the package class, whereas build phase functions like ``configure``, ``build`` and ``install``, and helper functions such as ``cmake_args`` or ``configure_args`` go into the builder classes.

.. note::

   The signature of certain methods changes when moving from a single build system to multiple build systems.

   Suppose you add support for CMake in the following Autotools package:

   .. code-block:: python

      from spack.package import *
      from spack_repo.builtin.build_systems import autotools


      class Example(autotools.AutotoolsPackage):
          def install(self, spec: Spec, prefix: str) -> None:
              # ...existing code...
              pass
   
   Then you should move the install method to the appropriate builder class, and change its signature:

   .. code-block:: python

      from spack.package import *
      from spack_repo.builtin.build_systems import autotools, cmake


      class Example(autotools.AutotoolsPackage, cmake.CMakePackage):
          build_system("autotools", "cmake", default="cmake")


      class AutotoolsBuilder(autotools.AutotoolsBuilder):
          def install(self, pkg: Example, spec: Spec, prefix: str) -> None:
              # ...existing code...
              pass

   Notice that the install method now takes the package instance as the first argument.
   This is because ``self`` refers to the builder class, not the package class.

Build dependencies typically depend on the choice of the build system.
An effective way to handle this is to use a ``with when("build_system=...")`` block to specify dependencies that are only relevant for a specific build system.

.. code-block:: python

   from spack.package import *
   from spack_repo.builtin.build_systems import cmake, autotools


   class Example(cmake.CMakePackage, autotools.AutotoolsPackage):

       build_system("cmake", "autotools", default="cmake")

       # Runtime dependencies
       depends_on("ncurses")
       depends_on("libxml2")

       # Lowerbounds for cmake only apply when using cmake as the build system
       with when("build_system=cmake"):
           depends_on("cmake@3.18:", when="@2.0:", type="build")
           depends_on("cmake@3:", type="build")

       # Specify extra build dependencies used only in the configure script
       with when("build_system=autotools"):
           depends_on("perl", type="build")
           depends_on("pkgconfig", type="build")

In the previous example, users could pick the desired build system at install time by specifying the ``build_system`` variant.
Much more commonly, packages transition from one build system to another from one version to the next.
That is, a package might use Autotools in version ``0.63`` and CMake in version ``0.64``.
In such cases we have to use the ``build_system`` directive to indicate when which build system can be used:

.. code-block:: python

   from spack.package import *
   from spack_repo.builtin.build_systems import cmake, autotools


   class Example(cmake.CMakePackage, autotools.AutotoolsPackage):

       build_system(
           conditional("cmake", when="@0.64:"),
           conditional("autotools", when="@:0.63"),
           default="cmake",
       )

In the example, the directive imposes a change from ``Autotools`` to ``CMake`` going from ``v0.63`` to ``v0.64``.

We have seen how users can run ``spack install example build_system=cmake`` to pick the desired build system.
The same can be done in ``depends_on`` statements, which has certain use cases.
A notable example is when a CMake package *needs* a CMake config file for its dependency, which is only generated when the dependency is built with CMake (and not Autotools).
In that case, you can *force* the choice of the build system of the dependency:

.. code-block:: python

   class Dependent(CMakePackage):

       depends_on("example build_system=cmake")

.. _make-package-findable:

Making a package discoverable with ``spack external find``
----------------------------------------------------------

The simplest way to make a package discoverable with :ref:`spack external find <cmd-spack-external-find>` is to:

1. Define the executables associated with the package.
2. Implement a method to determine the versions of these executables.

Minimal detection
^^^^^^^^^^^^^^^^^

The first step is fairly simple, as it requires only to specify a package-level ``executables`` attribute:

.. code-block:: python

   class Foo(Package):
       # Each string provided here is treated as a regular expression, and
       # would match for example "foo", "foobar", and "bazfoo".
       executables = ["foo"]

This attribute must be a list of strings.
Each string is a regular expression (e.g. "gcc" would match "gcc", "gcc-8.3", "my-weird-gcc", etc.) to determine a set of system executables that might be part of this package.
Note that to match only executables named "gcc" the regular expression ``"^gcc$"`` must be used.

Finally, to determine the version of each executable the ``determine_version`` method must be implemented:

.. code-block:: python

   @classmethod
   def determine_version(cls, exe):
       """Return either the version of the executable passed as argument
       or ``None`` if the version cannot be determined.

       Args:
           exe (str): absolute path to the executable being examined
       """

This method receives as input the path to a single executable and must return as output its version as a string.
If the version cannot be determined, or if the executable turns out to be a false positive, the value ``None`` must be returned, which ensures that the executable is discarded as a candidate.
Implementing the two steps above is mandatory, and gives the package the basic ability to detect if a spec is present on the system at a given version.

.. note::
   Any executable for which the ``determine_version`` method returns ``None`` will be discarded and won't appear in later stages of the workflow described below.

Additional functionality
^^^^^^^^^^^^^^^^^^^^^^^^

Besides the two mandatory steps described above, there are also optional methods that can be implemented to either increase the amount of details being detected or improve the robustness of the detection logic in a package.

Variants and custom attributes
""""""""""""""""""""""""""""""

The ``determine_variants`` method can be optionally implemented in a package to detect additional details of the spec:

.. code-block:: python

   @classmethod
   def determine_variants(cls, exes, version_str):
       """Return either a variant string, a tuple of a variant string
       and a dictionary of extra attributes that will be recorded in
       packages.yaml or a list of those items.

       Args:
           exes (list of str): list of executables (absolute paths) that
               live in the same prefix and share the same version
           version_str (str): version associated with the list of
               executables, as detected by ``determine_version``
       """

This method takes as input a list of executables that live in the same prefix and share the same version string, and returns either:

1. A variant string
2. A tuple of a variant string and a dictionary of extra attributes
3. A list of items matching either 1 or 2 (if multiple specs are detected from the set of executables)

If extra attributes are returned, they will be recorded in ``packages.yaml`` and be available for later reuse.
As an example, the ``gcc`` package will record by default the different compilers found and an entry in ``packages.yaml`` would look like:

.. code-block:: yaml

   packages:
     gcc:
       externals:
       - spec: "gcc@9.0.1 languages=c,c++,fortran"
         prefix: /usr
         extra_attributes:
           compilers:
             c: /usr/bin/x86_64-linux-gnu-gcc-9
             c++: /usr/bin/x86_64-linux-gnu-g++-9
             fortran: /usr/bin/x86_64-linux-gnu-gfortran-9

This allows us, for instance, to keep track of executables that would be named differently if built by Spack (e.g. ``x86_64-linux-gnu-gcc-9`` instead of just ``gcc``).

.. TODO: we need to gather some more experience on overriding "prefix"
   and other special keywords in extra attributes, but as soon as we are
   confident that this is the way to go we should document the process.
   See https://github.com/spack/spack/pull/16526#issuecomment-653783204

Filter matching executables
"""""""""""""""""""""""""""

Sometimes defining the appropriate regex for the ``executables`` attribute might prove to be difficult, especially if one has to deal with corner cases or exclude "red herrings".
To help keep the regular expressions as simple as possible, each package can optionally implement a ``filter_detected_exes`` method:

.. code-block:: python

    @classmethod
    def filter_detected_exes(cls, prefix, exes_in_prefix):
        """Return a filtered list of the executables in prefix"""

which takes as input a prefix and a list of matching executables and returns a filtered list of said executables.

Using this method has the advantage of allowing custom logic for filtering, and does not restrict the user to regular expressions only.
Consider the case of detecting the GNU C++ compiler.
If we try to search for executables that match ``g++``, that would have the unwanted side effect of selecting also ``clang++`` - which is a C++ compiler provided by another package - if present on the system.
Trying to select executables that contain ``g++`` but not ``clang`` would be quite complicated to do using only regular expressions.
Employing the ``filter_detected_exes`` method it becomes:

.. code-block:: python

   class Gcc(Package):
       executables = ["g++"]

       @classmethod
       def filter_detected_exes(cls, prefix, exes_in_prefix):
           return [x for x in exes_in_prefix if "clang" not in x]

Another possibility that this method opens is to apply certain filtering logic when specific conditions are met (e.g. take some decisions on an OS and not on another).

Validate detection
^^^^^^^^^^^^^^^^^^

To increase detection robustness, packagers may also implement a method to validate the detected Spec objects:

.. code-block:: python

   @classmethod
   def validate_detected_spec(cls, spec, extra_attributes):
       """Validate a detected spec. Raise an exception if validation fails."""

This method receives a detected spec along with its extra attributes and can be used to check that certain conditions are met by the spec.
Packagers can either use assertions or raise an ``InvalidSpecDetected`` exception when the check fails.
If the conditions are not honored the spec will be discarded and any message associated with the assertion or the exception will be logged as the reason for discarding it.

As an example, a package that wants to check that the ``compilers`` attribute is in the extra attributes can implement this method like this:

.. code-block:: python

   @classmethod
   def validate_detected_spec(cls, spec, extra_attributes):
       """Check that "compilers" is in the extra attributes."""
       msg = "the extra attribute 'compilers' must be set for the detected spec '{0}'".format(spec)
       assert "compilers" in extra_attributes, msg

or like this:

.. code-block:: python

   @classmethod
   def validate_detected_spec(cls, spec, extra_attributes):
       """Check that "compilers" is in the extra attributes."""
       if "compilers" not in extra_attributes:
           msg = "the extra attribute 'compilers' must be set for the detected spec '{0}'".format(
               spec
           )
           raise InvalidSpecDetected(msg)

.. _determine_spec_details:

Custom detection workflow
^^^^^^^^^^^^^^^^^^^^^^^^^

In the rare case when the mechanisms described so far don't fit the detection of a package, the implementation of all the methods above can be disregarded and instead a custom ``determine_spec_details`` method can be implemented directly in the package class (note that the definition of the ``executables`` attribute is still required):

.. code-block:: python

   @classmethod
   def determine_spec_details(cls, prefix, exes_in_prefix):
       # exes_in_prefix = a set of paths, each path is an executable
       # prefix = a prefix that is common to each path in exes_in_prefix

       # return None or [] if none of the exes represent an instance of
       # the package. Return one or more Specs for each instance of the
       # package which is thought to be installed in the provided prefix
       ...

This method takes as input a set of discovered executables (which match those specified by the user) as well as a common prefix shared by all of those executables.
The function must return one or more :py:class:`spack.package.Spec` associated with the executables (it can also return ``None`` to indicate that no provided executables are associated with the package).

As an example, consider a made-up package called ``foo-package`` which builds an executable called ``foo``.
``FooPackage`` would appear as follows:

.. code-block:: python

   class FooPackage(Package):
       homepage = "..."
       url = "..."

       version(...)

       # Each string provided here is treated as a regular expression, and
       # would match for example "foo", "foobar", and "bazfoo".
       executables = ["foo"]

       @classmethod
       def determine_spec_details(cls, prefix, exes_in_prefix):
           candidates = [x for x in exes_in_prefix if os.path.basename(x) == "foo"]
           if not candidates:
               return
           # This implementation is lazy and only checks the first candidate
           exe_path = candidates[0]
           exe = Executable(exe_path)
           output = exe("--version", output=str, error=str)
           version_str = ...  # parse output for version string
           return Spec.from_detection("foo-package@{0}".format(version_str))

Add detection tests to packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To ensure that software is detected correctly for multiple configurations and on different systems users can write a ``detection_test.yaml`` file and put it in the package directory alongside the ``package.py`` file.
This YAML file contains enough information for Spack to mock an environment and try to check if the detection logic yields the results that are expected.

As a general rule, attributes at the top-level of ``detection_test.yaml`` represent search mechanisms and they each map to a list of tests that should confirm the validity of the package's detection logic.

The detection tests can be run with the following command:

.. code-block:: console

   $ spack audit externals

Errors that have been detected are reported to screen.

Tests for PATH inspections
""""""""""""""""""""""""""

Detection tests insisting on ``PATH`` inspections are listed under the ``paths`` attribute:

.. code-block:: yaml

   paths:
   - layout:
     - executables:
       - "bin/clang-3.9"
       - "bin/clang++-3.9"
       script: |
         echo "clang version 3.9.1-19ubuntu1 (tags/RELEASE_391/rc2)"
         echo "Target: x86_64-pc-linux-gnu"
         echo "Thread model: posix"
         echo "InstalledDir: /usr/bin"
     platforms: ["linux", "darwin"]
     results:
     - spec: "llvm@3.9.1 +clang~lld~lldb"

If the ``platforms`` attribute is present, tests are run only if the current host matches one of the listed platforms.
Each test is performed by first creating a temporary directory structure as specified in the corresponding ``layout`` and by then running package detection and checking that the outcome matches the expected ``results``.
The exact details on how to specify both the ``layout`` and the ``results`` are reported in the table below:

.. list-table:: Test based on PATH inspections
   :header-rows: 1

   * - Option Name
     - Description
     - Allowed Values
     - Required Field
   * - ``layout``
     - Specifies the filesystem tree used for the test
     - List of objects
     - Yes
   * - ``layout:[0]:executables``
     - Relative paths for the mock executables to be created
     - List of strings
     - Yes
   * - ``layout:[0]:script``
     - Mock logic for the executable
     - Any valid shell script
     - Yes
   * - ``results``
     - List of expected results
     - List of objects (empty if no result is expected)
     - Yes
   * - ``results:[0]:spec``
     - A spec that is expected from detection
     - Any valid spec
     - Yes
   * - ``results:[0]:extra_attributes``
     - Extra attributes expected on the associated Spec
     - Nested dictionary with string as keys, and regular expressions as leaf values
     - No

Reuse tests from other packages
"""""""""""""""""""""""""""""""

When using a custom repository, it is possible to customize a package that already exists in ``builtin`` and reuse its external tests.
To do so, just write a ``detection_test.yaml`` alongside the customized ``package.py`` with an ``includes`` attribute.
For instance the ``detection_test.yaml`` for ``myrepo.llvm`` might look like:

.. code-block:: yaml

   includes:
   - "builtin.llvm"

This YAML file instructs Spack to run the detection tests defined in ``builtin.llvm`` in addition to those locally defined in the file.

.. _abi_compatibility:

Specifying ABI Compatibility
----------------------------

.. warning::

   The ``can_splice`` directive is experimental, and may be replaced by a higher-level interface in future versions of Spack.

Packages can include ABI-compatibility information using the ``can_splice`` directive.
For example, if ``Foo`` version 1.1 can always replace version 1.0, then the package could have:

.. code-block:: python

   can_splice("foo@1.0", when="@1.1")

For virtual packages, packages can also specify ABI compatibility with other packages providing the same virtual.
For example, ``zlib-ng`` could specify:

.. code-block:: python

   can_splice("zlib@1.3.1", when="@2.2+compat")

Some packages have ABI-compatibility that is dependent on matching variant values, either for all variants or for some set of ABI-relevant variants.
In those cases, it is not necessary to specify the full combinatorial explosion.
The ``match_variants`` keyword can cover all single-value variants.

.. code-block:: python

   # any value for bar as long as they're the same
   can_splice("foo@1.1", when="@1.2", match_variants=["bar"])

   # any variant values if all single-value variants match
   can_splice("foo@1.2", when="@1.3", match_variants="*")

The concretizer will use ABI compatibility to determine automatic splices when :ref:`automatic splicing<automatic_splicing>` is enabled.

Customizing Views
-----------------

.. warning::

   This is advanced functionality documented for completeness, and rarely needs customization.

Spack environments manage a view of their packages, which is a single directory that merges all installed packages through symlinks, so users can easily access them.
The methods of ``PackageViewMixin`` can be overridden to customize how packages are added to views.
Sometimes it's impossible to get an application to work just through symlinking its executables, and patching is necessary.
For example, Python scripts in a ``bin`` directory may have a shebang that points to the Python interpreter in Python's install prefix and not to the Python interpreter in the view.
However, it's more convenient to have the shebang point to the Python interpreter in the view, since that interpreter can locate other Python packages in the view without ``PYTHONPATH`` being set.
Therefore, Python extension packages (those inheriting from ``PythonPackage``) override ``add_files_to_view`` in order to rewrite shebang lines.
