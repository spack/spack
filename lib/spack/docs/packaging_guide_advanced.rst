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

================================
Packaging Guide: advanced topics
================================

This section of the packaging guide covers a few advanced topics.

.. _multiple_build_systems:

----------------------
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
           return [
               self.define_from_variant("MY_FEATURE", "my_feature")
           ]

   class AutotoolsBuilder(autotools.AutotoolsBuilder):
       def configure_args(self):
           return self.with_or_without("my-feature", variant="my_feature")

When defining a package like this, Spack automatically makes the ``build_system`` **variant** available, which can be used to pick the desired build system at install time.
For example

.. code-block:: console

   $ spack install example +feature build_system=cmake

makes Spack pick the ``CMakeBuilder`` class and runs ``cmake -DMY_FEATURE:BOOL=ON``.

Similarly

.. code-block:: console

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

In the example the directive imposes a change from ``Autotools`` to ``CMake`` going from ``v0.63`` to ``v0.64``.

We have seen how users can run ``spack install example build_system=cmake`` to pick the desired build system.
The same can be done in ``depends_on`` statements, which has certain use cases.
A notable example is when a CMake package *needs* a CMake config file for its dependency, which is only generated when the dependency is built with CMake (and not Autotools).
In that case, you can *force* the choice of the build system of the dependency:

.. code-block:: python

   class Dependent(CMakePackage):

       depends_on("example build_system=cmake")

.. _make-package-findable:

----------------------------------------------------------
Making a package discoverable with ``spack external find``
----------------------------------------------------------

The simplest way to make a package discoverable with
:ref:`spack external find <cmd-spack-external-find>` is to:

1. Define the executables associated with the package.
2. Implement a method to determine the versions of these executables.

^^^^^^^^^^^^^^^^^
Minimal detection
^^^^^^^^^^^^^^^^^

The first step is fairly simple, as it requires only to
specify a package-level ``executables`` attribute:

.. code-block:: python

   class Foo(Package):
       # Each string provided here is treated as a regular expression, and
       # would match for example "foo", "foobar", and "bazfoo".
       executables = ["foo"]

This attribute must be a list of strings. Each string is a regular
expression (e.g. "gcc" would match "gcc", "gcc-8.3", "my-weird-gcc", etc.) to
determine a set of system executables that might be part of this package. Note
that to match only executables named "gcc" the regular expression ``"^gcc$"``
must be used.

Finally, to determine the version of each executable the ``determine_version``
method must be implemented:

.. code-block:: python

   @classmethod
   def determine_version(cls, exe):
       """Return either the version of the executable passed as argument
       or ``None`` if the version cannot be determined.

       Args:
           exe (str): absolute path to the executable being examined
       """

This method receives as input the path to a single executable and must return
as output its version as a string; if the user cannot determine the version
or determines that the executable is not an instance of the package, they can
return None and the executable will be discarded as a candidate.
Implementing the two steps above is mandatory, and gives the package the
basic ability to detect if a spec is present on the system at a given version.

.. note::
   Any executable for which the ``determine_version`` method returns ``None``
   will be discarded and won't appear in later stages of the workflow described below.

^^^^^^^^^^^^^^^^^^^^^^^^
Additional functionality
^^^^^^^^^^^^^^^^^^^^^^^^

Besides the two mandatory steps described above, there are also optional
methods that can be implemented to either increase the amount of details
being detected or improve the robustness of the detection logic in a package.

""""""""""""""""""""""""""""""
Variants and custom attributes
""""""""""""""""""""""""""""""

The ``determine_variants`` method can be optionally implemented in a package
to detect additional details of the spec:

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

This method takes as input a list of executables that live in the same prefix and
share the same version string, and returns either:

1. A variant string
2. A tuple of a variant string and a dictionary of extra attributes
3. A list of items matching either 1 or 2 (if multiple specs are detected
   from the set of executables)

If extra attributes are returned, they will be recorded in ``packages.yaml``
and be available for later reuse. As an example, the ``gcc`` package will record
by default the different compilers found and an entry in ``packages.yaml``
would look like:

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

This allows us, for instance, to keep track of executables that would be named
differently if built by Spack (e.g. ``x86_64-linux-gnu-gcc-9``
instead of just ``gcc``).

.. TODO: we need to gather some more experience on overriding "prefix"
   and other special keywords in extra attributes, but as soon as we are
   confident that this is the way to go we should document the process.
   See https://github.com/spack/spack/pull/16526#issuecomment-653783204

"""""""""""""""""""""""""""
Filter matching executables
"""""""""""""""""""""""""""

Sometimes defining the appropriate regex for the ``executables``
attribute might prove to be difficult, especially if one has to
deal with corner cases or exclude "red herrings". To help keep
the regular expressions as simple as possible, each package can
optionally implement a ``filter_detected_exes`` method:

.. code-block:: python

    @classmethod
    def filter_detected_exes(cls, prefix, exes_in_prefix):
        """Return a filtered list of the executables in prefix"""

which takes as input a prefix and a list of matching executables and
returns a filtered list of said executables.

Using this method has the advantage of allowing custom logic for
filtering, and does not restrict the user to regular expressions
only.  Consider the case of detecting the GNU C++ compiler. If we
try to search for executables that match ``g++``, that would have
the unwanted side effect of selecting also ``clang++`` - which is
a C++ compiler provided by another package - if present on the system.
Trying to select executables that contain ``g++`` but not ``clang``
would be quite complicated to do using regex only. Employing the
``filter_detected_exes`` method it becomes:

.. code-block:: python

   class Gcc(Package):
      executables = ["g++"]

      @classmethod
      def filter_detected_exes(cls, prefix, exes_in_prefix):
         return [x for x in exes_in_prefix if "clang" not in x]

Another possibility that this method opens is to apply certain
filtering logic when specific conditions are met (e.g. take some
decisions on an OS and not on another).

^^^^^^^^^^^^^^^^^^
Validate detection
^^^^^^^^^^^^^^^^^^

To increase detection robustness, packagers may also implement a method
to validate the detected Spec objects:

.. code-block:: python

   @classmethod
   def validate_detected_spec(cls, spec, extra_attributes):
       """Validate a detected spec. Raise an exception if validation fails."""

This method receives a detected spec along with its extra attributes and can be
used to check that certain conditions are met by the spec. Packagers can either
use assertions or raise an ``InvalidSpecDetected`` exception when the check fails.
If the conditions are not honored the spec will be discarded and any message
associated with the assertion or the exception will be logged as the reason for
discarding it.

As an example, a package that wants to check that the ``compilers`` attribute is
in the extra attributes can implement this method like this:

.. code-block:: python

   @classmethod
   def validate_detected_spec(cls, spec, extra_attributes):
       """Check that "compilers" is in the extra attributes."""
       msg = ("the extra attribute 'compilers' must be set for "
              "the detected spec '{0}'".format(spec))
       assert "compilers" in extra_attributes, msg

or like this:

.. code-block:: python

   @classmethod
   def validate_detected_spec(cls, spec, extra_attributes):
       """Check that "compilers" is in the extra attributes."""
       if "compilers" not in extra_attributes:
           msg = ("the extra attribute 'compilers' must be set for "
                  "the detected spec '{0}'".format(spec))
           raise InvalidSpecDetected(msg)

.. _determine_spec_details:

^^^^^^^^^^^^^^^^^^^^^^^^^
Custom detection workflow
^^^^^^^^^^^^^^^^^^^^^^^^^

In the rare case when the mechanisms described so far don't fit the
detection of a package, the implementation of all the methods above
can be disregarded and instead a custom ``determine_spec_details``
method can be implemented directly in the package class (note that
the definition of the ``executables`` attribute is still required):

.. code-block:: python

   @classmethod
   def determine_spec_details(cls, prefix, exes_in_prefix):
       # exes_in_prefix = a set of paths, each path is an executable
       # prefix = a prefix that is common to each path in exes_in_prefix

       # return None or [] if none of the exes represent an instance of
       # the package. Return one or more Specs for each instance of the
       # package which is thought to be installed in the provided prefix

This method takes as input a set of discovered executables (which match
those specified by the user) as well as a common prefix shared by all
of those executables. The function must return one or more :py:class:`spack.package.Spec` associated
with the executables (it can also return ``None`` to indicate that no
provided executables are associated with the package).

As an example, consider a made-up package called ``foo-package`` which
builds an executable called ``foo``. ``FooPackage`` would appear as
follows:

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
           candidates = list(x for x in exes_in_prefix
                             if os.path.basename(x) == "foo")
           if not candidates:
               return
           # This implementation is lazy and only checks the first candidate
           exe_path = candidates[0]
           exe = Executable(exe_path)
           output = exe("--version", output=str, error=str)
           version_str = ...  # parse output for version string
           return Spec.from_detection(
               "foo-package@{0}".format(version_str)
           )

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Add detection tests to packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To ensure that software is detected correctly for multiple configurations
and on different systems users can write a ``detection_test.yaml`` file and
put it in the package directory alongside the ``package.py`` file.
This YAML file contains enough information for Spack to mock an environment
and try to check if the detection logic yields the results that are expected.

As a general rule, attributes at the top-level of ``detection_test.yaml``
represent search mechanisms and they each map to a list of tests that should confirm
the validity of the package's detection logic.

The detection tests can be run with the following command:

.. code-block:: console

   $ spack audit externals

Errors that have been detected are reported to screen.

""""""""""""""""""""""""""
Tests for PATH inspections
""""""""""""""""""""""""""

Detection tests insisting on ``PATH`` inspections are listed under
the ``paths`` attribute:

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
     - spec: 'llvm@3.9.1 +clang~lld~lldb'

If the ``platforms`` attribute is present, tests are run only if the current host
matches one of the listed platforms.
Each test is performed by first creating a temporary directory structure as
specified in the corresponding ``layout`` and by then running
package detection and checking that the outcome matches the expected
``results``. The exact details on how to specify both the ``layout`` and the
``results`` are reported in the table below:

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

"""""""""""""""""""""""""""""""
Reuse tests from other packages
"""""""""""""""""""""""""""""""

When using a custom repository, it is possible to customize a package that already exists in ``builtin``
and reuse its external tests. To do so, just write a ``detection_test.yaml`` alongside the customized
``package.py`` with an ``includes`` attribute. For instance the ``detection_test.yaml`` for
``myrepo.llvm`` might look like:

.. code-block:: yaml

   includes:
   - "builtin.llvm"

This YAML file instructs Spack to run the detection tests defined in ``builtin.llvm`` in addition to
those locally defined in the file.

.. _source-code-from-vcs:

----------------------------------------
Source code from version control systems
----------------------------------------

As mentioned in :doc:`packaging_guide_creation`, Spack supports fetching source code from various version control systems (VCS).
Here we list the various options available for each of the supported VCS.

.. _git-fetch:

^^^^^^^
Git
^^^^^^^

Git fetching supports the following parameters to the ``version`` directive:

* ``git``: URL of the git repository, if different than the class-level ``git``.
* ``branch``: Name of a :ref:`branch <git-branches>` to fetch.
* ``tag``: Name of a :ref:`tag <git-tags>` to fetch.
* ``commit``: SHA hash (or prefix) of a :ref:`commit <git-commits>` to fetch.
* ``submodules``: Also fetch :ref:`submodules <git-submodules>` recursively when checking out this repository.
* ``submodules_delete``: A list of submodules to forcibly delete from the repository
  after fetching. Useful if a version in the repository has submodules that
  have disappeared/are no longer accessible.
* ``get_full_repo``: Ensure the full git history is checked out with all remote
  branch information. Normally (``get_full_repo=False``, the default), the git
  option ``--depth 1`` will be used if the version of git and the specified
  transport protocol support it, and ``--single-branch`` will be used if the
  version of git supports it.
* ``git_sparse_paths``: Only clone the provided :ref:`relative paths <git-sparse-checkout>`.

The destination directory for the clone is the standard stage source path.

.. note::

   ``tag`` and ``branch`` should not be combined in the version parameters.

   We strongly recommend that all ``tag`` entries be paired with ``commit``.


.. warning::

   **Trusted Downloads.**
   It is critical from a security and reproducibility standpoint that Spack be able to verify the downloaded source.

   Providing the full ``commit`` SHA hash allows for Spack to preserve binary provenance for all binaries since git commits are guaranteed to be unique points in the git history.
   Whereas, the mutable nature of branches and tags cannot provide such a guarantee.

   A git download *is trusted* only if the full commit SHA is specified.
   Therefore, it is *the* recommended way to securely download from a Git repository.


.. _git-default-branch:

Default branch
  A version with only a name results in fetching a repository's default branch:

  .. code-block:: python

     class Example(Package):

         git = "https://github.com/example-project/example.git"

         version("develop")

  Aside from use of HTTPS, there is no way to verify that the repository has not been compromised.
  Furthermore, the commit you get when you install the package likely won't be the same commit that was used when the package was first written.
  There is also the risk that the default branch may change.

  .. warning::

    This download method is **untrusted**, and is **not recommended**.

    It is better to specify a branch name (see :ref:`below <git-branches>`).


.. _git-branches:

Branches
  To fetch a particular branch, use the ``branch`` parameter, preferrably with the same name as the version.
  For example,

  .. code-block:: python

     version("main", branch="main")
     version("experimental", branch="experimental")

  Branches are moving targets, which means the commit you get when you install the package likely won't be the one used when the package was first written.

  .. note::

     Common branch names are special in terms of how Spack determines the latest version of a package.
     See "infinity versions" in :ref:`version ordering <version-comparison>` for more information.

  .. warning::

    This download method is **untrusted**, and is **not recommended** for production installations.


.. _git-tags:

Tags
  To fetch from a particular tag, use ``tag`` instead:

  .. code-block:: python

     version("1.0.1", tag="v1.0.1")

  While tags are generally more stable than branches, Git allows tags to be moved.
  Many developers use tags to denote rolling releases, and may move the tag when a bug is fixed.

  .. warning::

    This download method is **untrusted**, and is **not recommended**.

    If you must use a ``tag``, it is recommended to combine it with the ``commit`` option (see :ref:`below <git-commits>`).


.. _git-commits:

Commits
  To fetch a particular commit, use the ``commit`` argument:

  .. code-block:: python

     version("2014-10-08", commit="1e6ef73d93a28240f954513bc4c2ed46178fa32b")
     version("1.0.4", tag="v1.0.4", commit="420136f6f1f26050d95138e27cf8bc905bc5e7f52")   

  It may be useful to provide a saner version for commits like this, e.g., you might use the date as the version, as done in the first example above.
  Or, if you know the commit at which a release was cut, you can use the release version.
  It is up to the package author to decide which of these options makes the most sense.

  .. warning::

    A git download is *trusted only if* the **full commit sha** is specified.


  .. hint::

     **Avoid using the commit hash as the version.**
     It is not recommended to use the commit hash as the version itself, since it won't sort properly for :ref:`version ordering <version-comparison>` purposes.


.. _git-submodules:

Submodules
  You can supply ``submodules=True`` to cause Spack to fetch submodules recursively along with the repository.

  .. code-block:: python

     version("1.1.0", commit="907d5f40d653a73955387067799913397807adf3", submodules=True)

  If a package needs more fine-grained control over submodules, define ``submodules`` to be a callable function that takes the package instance as its only argument.
  The function needs to return a list of submodules to be fetched.

  .. code-block:: python

     def submodules(package):
         submodules = []
         if "+variant-1" in package.spec:
             submodules.append("submodule_for_variant_1")
         if "+variant-2" in package.spec:
             submodules.append("submodule_for_variant_2")
         return submodules


      class MyPackage(Package):
          version("1.1.0", commit="907d5f40d653a73955387067799913397807adf3", submodules=submodules)

  For more information about git submodules see the man page of git: ``man git-submodule``.


.. _git-sparse-checkout:

Sparse-Checkout
  If you only want to clone a subset of the contents of a git repository, you can supply ``git_sparse_paths`` at the package or version level to utilize git's sparse-checkout feature.
  The paths can be specified through an attribute, property or callable function.
  This option is useful for large repositories containing separate features that can be built independently.

  .. note::

     This leverages a newer feature in git that requires version ``2.25.0`` or greater.

     If ``git_sparse_paths`` is supplied to a git version that is too old then a warning will be issued before standard cloning operations are performed.

  .. note::

     Paths to directories result in the cloning of *all* of their contents, including the contents of their subdirectories.

  The ``git_sparse_paths`` attribute needs to provide a list of relative paths within the repository.
  If using a property -- a function decorated with ``@property`` -- or an argument that is a callable function, the function needs to return a list of paths.

  For example, using the attribute approach:

  .. code-block:: python

    class MyPackage(package):
        # using an attribute
        git_sparse_paths = ["doe", "rae"]

        version("1.0.0")
        version("1.1.0")

  results in the files from the top level directory of the repository and the contents of the ``doe`` and ``rae`` relative paths within the repository to be cloned.

  Alternatively, you can provide the paths to the version directive argument using a callable function whose return value is a list for paths. 
  For example:

  .. code-block:: python

    def sparse_path_function(package)
        paths = ["doe", "rae", "me/file.cpp"]
        if package.spec.version >  Version("1.2.0"):
            paths.extend(["fae"])
        return paths

    class MyPackage(package):
        version("1.1.5", git_sparse_paths=sparse_path_function)
        version("1.2.0", git_sparse_paths=sparse_path_function)
        version("1.2.5", git_sparse_paths=sparse_path_function)
        version("1.1.5", git_sparse_paths=sparse_path_function)

  results in the cloning of the files from the top level directory of the repository, the contents of the ``doe`` and ``rae`` relative paths, *and* the ``me/file.cpp`` file. If the package version is greater than ``1.2.0`` then the contents of the ``fae`` relative path will also be cloned.

  .. note::

     The version directives in the examples above are simplified to emphasize use of this feature.
     Trusted downloads require a hash, such as a :ref:`sha256 <github-fetch>` or :ref:`commit <git-commits>`.


.. _github-fetch:

^^^^^^
GitHub
^^^^^^

If a project is hosted on GitHub, *any* valid Git branch, tag, or hash
may be downloaded as a tarball.  This is accomplished simply by
constructing an appropriate URL.  Spack can checksum any package
downloaded this way, thereby producing a trusted download.  For
example, the following downloads a particular hash, and then applies a
checksum.

.. code-block:: python

       version(
           "1.9.5.1.1",
           sha256="8d74beec1be996322ad76813bafb92d40839895d6dd7ee808b17ca201eac98be",
           url="https://www.github.com/jswhit/pyproj/tarball/0be612cc9f972e38b50a90c946a9b353e2ab140f",
       )

Alternatively, you could provide the GitHub ``url`` for one version as a property and Spack will extrapolate the URL for other versions as described in :ref:`Versions and URLs <versions-and-fetching>`.


.. _hg-fetch:

^^^^^^^^^
Mercurial
^^^^^^^^^

Fetching with Mercurial works much like `Git <git-fetch>`_, but you
use the ``hg`` parameter.
The destination directory is still the standard stage source path.

.. _hg-default-branch:

Default branch
  Add the ``hg`` attribute with no ``revision`` passed to ``version``:

  .. code-block:: python

     class Example(Package):

         hg = "https://bitbucket.org/example-project/example"

         version("develop")

  As with Git's default fetching strategy, there is no way to verify the integrity of the download.

  .. warning::

    This download method is **untrusted**, and is **not recommended**.


.. _hg-revisions:

Revisions
  To fetch a particular revision, use the ``revision`` parameter:

  .. code-block:: python

     version("1.0", revision="v1.0")

  Unlike ``git``, which has special parameters for different types of revisions, you can use ``revision`` for branches, tags, and **commits** when you fetch with Mercurial.

  .. warning::

    Like Git, fetching specific branches or tags is an **untrusted** download method, and is **not recommended**.

    The recommended fetch strategy is to specify a particular commit hash as the revision.


.. _svn-fetch:

^^^^^^^^^^
Subversion
^^^^^^^^^^

To fetch with subversion, use the ``svn`` and ``revision`` parameters.
The destination directory will be the standard stage source path.

Fetching the head
  Simply add an ``svn`` parameter to the package:

  .. code-block:: python

     class Example(Package):

         svn = "https://outreach.scidac.gov/svn/example/trunk"

         version("develop")

  .. warning::

    This download method is **untrusted**, and is **not recommended** for the same reasons as mentioned above.


.. _svn-revisions:

Fetching a revision
  To fetch a particular revision, add a ``revision`` argument to the
  version directive:

  .. code-block:: python

     version("develop", revision=128)

  Unfortunately, Subversion has no commit hashing scheme like Git and
  Mercurial do, so there is no way to guarantee that the download you
  get is the same as the download used when the package was created.
  Use at your own risk.

  .. warning::

    This download method is **untrusted**, and is **not recommended**.


Subversion branches are handled as part of the directory structure, so
you can check out a branch or tag by changing the URL. If you want to
package multiple branches, simply add a ``svn`` argument to each
version directive.


.. _cvs-fetch:

^^^^^^^
CVS
^^^^^^^

CVS (Concurrent Versions System) is an old centralized version control
system. It is a predecessor of Subversion.

To fetch with CVS, use the ``cvs``, branch, and ``date`` parameters.
The destination directory will be the standard stage source path.

.. _cvs-head:

Fetching the head
  Simply add a ``cvs`` parameter to the package:

  .. code-block:: python

     class Example(Package):

         cvs = ":pserver:outreach.scidac.gov/cvsroot%module=modulename"

         version("1.1.2.4")

  CVS repository locations are described using an older syntax that
  is different from today's ubiquitous URL syntax. ``:pserver:``
  denotes the transport method. CVS servers can host multiple
  repositories (called "modules") at the same location, and one needs
  to specify both the server location and the module name to access.
  Spack combines both into one string using the ``%module=modulename``
  suffix shown above.

  .. warning::

    This download method is **untrusted**.


.. _cvs-date:

Fetching a date
  Versions in CVS are commonly specified by date. To fetch a
  particular branch or date, add a ``branch`` and/or ``date`` argument
  to the version directive:

  .. code-block:: python

     version("2021.4.22", branch="branchname", date="2021-04-22")

  Unfortunately, CVS does not identify repository-wide commits via a
  revision or hash like Subversion, Git, or Mercurial do. This makes
  it impossible to specify an exact commit to check out.

  .. warning::

    This download method is **untrusted**.


CVS has more features, but since CVS is rarely used these days, Spack does not support all of them.

.. _abi_compatibility:

----------------------------
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

   can_splice("foo@1.1", when="@1.2", match_variants=["bar"])  # any value for bar as long as they're the same
   can_splice("foo@1.2", when="@1.3", match_variants="*")  # any variant values if all single-value variants match

The concretizer will use ABI compatibility to determine automatic splices when :ref:`automatic splicing<automatic_splicing>` is enabled.

-----------------
Customizing Views
-----------------

.. warning::

   This is advanced functionality documented for completeness, and rarely needs customization.

Spack environments manage a view of their packages, which is a single directory
that merges all installed packages through symlinks, so users can easily access them.
The methods of ``PackageViewMixin`` can be overridden to customize how packages are added
to views.
Sometimes it's impossible to get an application to work just through symlinking its executables, and patching is necessary.
For example, Python scripts in a ``bin`` directory may have a shebang that points to the Python interpreter in Python's install prefix, but it's more convenient to have the shebang point to the Python interpreter in the view, since that interpreter is aware of the Python packages in the view (the view is a virtual environment).
As a consequence, Python extension packages (those inheriting from ``PythonPackage``) override ``add_files_to_view`` in order to rewrite shebang lines.
